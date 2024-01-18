import os
import bcrypt
from fastapi import HTTPException, status
from jwt import encode, decode, DecodeError, ExpiredSignatureError
from datetime import datetime, timedelta
from dotenv import load_dotenv

from src.utils.exceptions import MissingEnvironmentVariable

load_dotenv(dotenv_path="src/config/env-files/.env.local")


def get_required_env_variable(name: str) -> str:
    """
    This function checks the value of the env variables.

    Parameters:
    - name (str): The name of the env variable.

    Returns:
    str: Returns value
    """
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise MissingEnvironmentVariable(
            f"Missing or empty '{name}' environment variable."
        )
    return value


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def generate_jwt_token(
    payload,
    secret_key=get_required_env_variable("JWT_SECRET_KEY"),
    expiration_time_hours=1,
    algorithm="HS256",
):
    expiration_time = datetime.utcnow() + timedelta(hours=expiration_time_hours)
    payload["exp"] = expiration_time
    return encode(payload, secret_key, algorithm=algorithm)


def decode_jwt_token(
    token, secret_key=get_required_env_variable("JWT_SECRET_KEY"), algorithms=["HS256"]
):
    try:
        payload = decode(token, secret_key, algorithms=algorithms)
        return payload
    except (DecodeError, ExpiredSignatureError):
        raise HTTPException(
            detail="Invalid Token!", status_code=status.HTTP_401_UNAUTHORIZED
        )
