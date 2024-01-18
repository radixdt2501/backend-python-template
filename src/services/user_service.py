import logging
from fastapi import Response, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy import insert, or_, select

from src.utils.types import RegisterUser, RegisterResponse, LoginUser, LoginResponse
from src.models.user_model import UserModel
from src.utils.index import generate_jwt_token, hash_password, verify_password
from src.config.database.db_connection import engine
from src.utils.exceptions import DatabaseException

logger = logging.getLogger(__name__)

def create_account(payload: RegisterUser, response: Response) -> RegisterResponse:
    """
    Create a user account with the provided registration payload.

    Parameters:
    - payload (RegisterUser): Registration payload.
    - response (Response): FastAPI Response object.

    Returns:
    RegisterResponse: Registration response.

    Raises:
    - DatabaseException: If there is an error in the database operation.
    """
    hashed_password = hash_password(payload.password)
    stmt = insert(UserModel).values(
        first_name=payload.firstName,
        last_name=payload.lastName,
        username=payload.username,
        email=payload.email,
        password=hashed_password,
        role=payload.role,
    )
    with engine.begin() as conn:
        try:
            result = conn.execute(stmt)
            return {
                "success": True,
                "message": "User Registered Successfully",
                "id": str(result.inserted_primary_key[0]),
            }
        except IntegrityError as error:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {"success": False, "message": "User Already Exists!", "id": None}
        except SQLAlchemyError as error:
            raise DatabaseException("Error during user registration") from error


def authenticate_user(payload: LoginUser, response: Response) -> LoginResponse:
    """
    Authenticate a user with the provided login payload.

    Parameters:
    - payload (LoginUser): Login payload.
    - response (Response): FastAPI Response object.

    Returns:
    LoginResponse: Login response.

    Raises:
    - SQLAlchemyError: If there is an error in the database operation.
    - Exception: For unexpected errors during user authentication.
    """
    try:
        query = (
            select(UserModel)
            .where(
                or_(
                    UserModel.email == payload.identifier,
                    UserModel.username == payload.identifier,
                )
            )
            .limit(1)
        )

        with engine.begin() as conn:
            result = conn.execute(query)
            user_data = result.fetchone()

            user_dict = dict(zip(result.keys(), user_data))

            is_password_verified = verify_password(
                payload.password, user_dict["password"]
            )

            if is_password_verified:
                user_payload = {
                    "id": str(user_dict["id"]),
                    "username": user_dict["username"],
                    "email": user_dict["email"],
                }
                jwt_token = generate_jwt_token(user_payload)
                response.set_cookie(
                    key="token",
                    value=jwt_token,
                    httponly=True,
                    samesite="strict",
                    secure=True,
                    expires=3600,
                )

                return {
                    "success": True,
                    "message": "User logged in successfully!",
                    "token": jwt_token,
                }
            else:
                return {
                    "success": False,
                    "message": "Username or password is incorrect!",
                    "token": None,
                }

    except SQLAlchemyError as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Error during user authentication")
        raise SQLAlchemyError("Error during user authentication") from error

    except Exception as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Unexpected error during user authentication")
        raise Exception("Unexpected error during user authentication") from error


def get_user_info_by_id(user_id: str, response: Response):
    """
    Retrieve user information by ID.

    Parameters:
    - user_id (str): User ID.
    - response (Response): FastAPI Response object.

    Returns:
    dict: User information.

    Raises:
    - SQLAlchemyError: If there is an error in the database operation.
    """
    try:
        query = (
            select(
                UserModel.id,
                UserModel.email,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.username,
                UserModel.role,
                UserModel.is_deleted,
                UserModel.is_verified,
            )
            .where(UserModel.id == user_id)
            .limit(1)
        )

        with engine.begin() as conn:
            result = conn.execute(query)
            user_data = result.fetchone()

            user_dict = dict(zip(result.keys(), user_data))
            user_dict["id"] = str(user_dict["id"])

            return {"success": True, "data": user_dict}

    except SQLAlchemyError as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Error during user retrieving data by id")
        raise SQLAlchemyError("Error during user retrieval by ID") from error


def get_all_users_with_pagination(response: Response, page: int = 1, page_size: int = 10):
    """
    Retrieve all users with pagination.

    Parameters:
    - response (Response): FastAPI Response object.
    - page (int): Page number (default: 1).
    - page_size (int): Number of items per page (default: 10).

    Returns:
    dict: Response containing the list of users.

    Raises:
    - NoResultFound: If no users are found.
    - SQLAlchemyError: If there is an error in the database operation.
    """
    try:
        skip = (page - 1) * page_size
        query = select(UserModel).offset(skip).limit(page_size)

        with engine.begin() as conn:
            result = conn.execute(query)
            # users_list = [dict((key, value) for key, value in zip(result.keys(), user) if key != "password") for user in result.fetchall()]
            users_list = [dict((key, str(value)) if key == "id" else (key, value) for key, value in zip(result.keys(), user) if key != "password") for user in result.fetchall()]

            return {"success": True, "data": users_list}

    except NoResultFound:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise NoResultFound("No users found") from None

    except SQLAlchemyError as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Error during user retrieving data by id")
        raise SQLAlchemyError("Error during user retrieval with pagination") from error
