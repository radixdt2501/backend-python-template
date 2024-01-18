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
            raise DatabaseException() from error


def authenticate_user(payload: LoginUser, response: Response) -> LoginResponse:
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
        return {"success": False, "message": str(error)}

    except Exception as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Unexpected error during user authentication")
        return {"success": False, "message": "An unexpected error occurred."}


def getUserInfoByID(userId: str, response: Response):
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
            .where(UserModel.id == userId)
            .limit(1)
        )

        with engine.begin() as conn:
            result = conn.execute(query)
            user_data = result.fetchone()

            user_dict = dict(zip(result.keys(), user_data))

            return {"success": True, "data": user_dict}

    except SQLAlchemyError as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Error during user retriving data by id")
        return {"success": False, "message": str(error)}


def getAllUsersWithPagination(response: Response, page: int = 1, page_size: int = 10):
    try:
        skip = (page - 1) * page_size
        query = select(UserModel).offset(skip).limit(page_size)

        with engine.begin() as conn:
            result = conn.execute(query)
            users_list = [dict((key, value) for key, value in zip(result.keys(), user) if key != "password") for user in result.fetchall()]

            return {"success": True, "data": users_list}

    except NoResultFound:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"success": False, "message": "No users found"}

    except SQLAlchemyError as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Error during user retrieving data by id")
        return {"success": False, "message": str(error)}
