import logging
from datetime import datetime, timezone
import os
from typing import Annotated, Dict
from fastapi import File, HTTPException, Response, UploadFile, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy import insert, or_, select, update

from src.utils.types import (
    RegisterUser,
    BaseSuccessResponse,
    LoginUser,
    LoginResponse,
)
from src.models.user_model import UserModel
from src.utils.index import generate_jwt_token, hash_password, verify_password
from src.config.database.db_connection import engine
from src.utils.exceptions import DatabaseException

logger = logging.getLogger(__name__)


def create_account(payload: RegisterUser, response: Response) -> BaseSuccessResponse:
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
        email=payload.email.lower(),
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
                    UserModel.email == payload.identifier.lower(),
                    UserModel.username == payload.identifier,
                )
            )
            .limit(1)
        )

        with engine.begin() as conn:
            result = conn.execute(query)
            user_data = result.fetchone()

            if user_data is None:
                raise HTTPException(
                    detail="This account is not registered with us!",
                    status_code=status.HTTP_404_NOT_FOUND,
                )

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

    except (SQLAlchemyError, NoResultFound) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Error during user authentication")
        raise HTTPException(detail="Error during user authentication") from error


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


def get_all_users_with_pagination(
    response: Response, page: int = 1, page_size: int = 10
):
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
            users_list = [
                dict(
                    (key, str(value)) if key == "id" else (key, value)
                    for key, value in zip(result.keys(), user)
                    if key != "password"
                )
                for user in result.fetchall()
            ]

            return {"success": True, "data": users_list}

    except NoResultFound:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise NoResultFound("No users found") from None

    except SQLAlchemyError as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception("Error during user retrieving data by id")
        raise SQLAlchemyError("Error during user retrieval with pagination") from error


def update_user_with_image(
    response: Response,
    user_info_extended: dict,
    file: Annotated[UploadFile, File()],
) -> Dict[str, any]:
    """
    Update user information along with the profile picture path.

    Parameters:
    - response (Response): FastAPI Response object.
    - user_info_extended (dict): User information payload.

    Returns:
    Dict[str, any]: Dictionary containing the success status, message, and user ID if successful.

    Raises:
    IntegrityError: If there is an integrity violation (e.g., unique constraint).
    SQLAlchemyError: If there is an error in the database operation.
    """
    try:
        payload = {}
        for key, val in user_info_extended.items():
            if val is not None:
                if key == "email":
                    payload[key] = val.lower()
                else:
                    payload[key] = val
        stmt = (
            update(UserModel)
            .where(UserModel.id == payload.get("id"))
            .values(
                **payload,
                updated_at=datetime.utcnow().replace(tzinfo=timezone.utc),
            )
        )
        with engine.begin() as conn:
            conn.execute(stmt)
            folder_path = "uploads"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            if file:
                file_path = os.path.join(folder_path, file.filename)
                with open(file_path, "wb") as local_file:
                    local_file.write(file.file.read())

        return {
            "success": True,
            "message": "User Updated Successfully",
            "id": str(payload.get("id")),
        }

    except IntegrityError as error:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {
            "success": False,
            "message": "User Already Exists with that information",
            "id": None,
        }

    except SQLAlchemyError as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"success": False, "message": "Failed to update user!", "id": None}
