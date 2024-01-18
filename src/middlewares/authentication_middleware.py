from typing import Annotated
from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from fastapi import HTTPException, status, Cookie
from jwt import DecodeError, ExpiredSignatureError
from src.models.user_model import UserModel

from src.config.database.db_connection import engine
from src.utils.index import decode_jwt_token


def verify_auth_token(token: Annotated[str | None, Cookie()] = None):
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
            user_dict = dict(zip(result.keys(), user_data))
            return user_dict

    except (KeyError, DecodeError, ExpiredSignatureError, NoResultFound):
        raise HTTPException(
            detail="Invalid Token!", status_code=status.HTTP_401_UNAUTHORIZED
        )
