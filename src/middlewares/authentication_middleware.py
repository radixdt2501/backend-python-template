from typing import Annotated, Optional

from fastapi import Cookie, HTTPException, status
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound

from src.config.database.db_connection import engine
from src.models.user_model import UserModel
from src.utils.index import decode_jwt_token


def verify_auth_token(token: Annotated[str | None, Cookie()] = None) -> Optional[dict]:
    """
    Verify the user's authentication token and retrieve user information.

    Parameters:
    - token (Annotated[str | None, Cookie()]): The authentication token from the request cookies.

    Returns:
    Optional[dict]: User information dictionary if the token is valid, None otherwise.

    Raises:
    - HTTPException: If the token is invalid or expired.
    """
    try:
        payload = decode_jwt_token(token)
        stmt = (
            select(
                UserModel.id,
                UserModel.email,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.username,
                UserModel.role,
            )
            .where(
                and_(
                    UserModel.id == payload["id"],
                    UserModel.email == payload["email"],
                    UserModel.username == payload["username"],
                )
            )
            .limit(1)
        )

        with engine.begin() as conn:
            result = conn.execute(stmt)
            user_data = result.fetchone()

            if user_data:
                user_dict = dict(zip(result.keys(), user_data))
                user_dict["id"] = str(user_dict["id"])
                return user_dict
            else:
                # User not found in the database
                return None

    except (KeyError, DecodeError, ExpiredSignatureError, NoResultFound):
        # Invalid or expired token
        raise HTTPException(
            detail="Invalid Token!", status_code=status.HTTP_401_UNAUTHORIZED
        )
