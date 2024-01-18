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
    Get the value of the specified environment variable.

    Parameters:
    - name (str): The name of the environment variable.

    Returns:
    str: The value of the environment variable.

    Raises:
    MissingEnvironmentVariable: If the environment variable is missing or empty.
    """
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise MissingEnvironmentVariable(
            f"Missing or empty '{name}' environment variable."
        )
    return value


def hash_password(password: str) -> str:
    """
    Hash the given password using bcrypt.

    Parameters:
    - password (str): The password to be hashed.

    Returns:
    str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the provided plain password matches the hashed password.

    Parameters:
    - plain_password (str): The plain text password.
    - hashed_password (str): The hashed password to be compared.

    Returns:
    bool: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def generate_jwt_token(
    payload,
    secret_key=get_required_env_variable("JWT_SECRET_KEY"),
    expiration_time_hours=1,
    algorithm="HS256",
) -> str:
    """
    Generate a JWT token with the provided payload.

    Parameters:
    - payload: The data to be included in the token.
    - secret_key (str): The secret key for signing the token.
    - expiration_time_hours (int): Token expiration time in hours.
    - algorithm (str): The hashing algorithm for the token.

    Returns:
    str: The generated JWT token.
    """
    expiration_time = datetime.utcnow() + timedelta(hours=expiration_time_hours)
    payload["exp"] = expiration_time
    return encode(payload, secret_key, algorithm=algorithm)


def decode_jwt_token(
    token, secret_key=get_required_env_variable("JWT_SECRET_KEY"), algorithms=["HS256"]
) -> dict:
    """
    Decode a JWT token.

    Parameters:
    - token (str): The JWT token to be decoded.
    - secret_key (str): The secret key for decoding the token.
    - algorithms (list): The list of allowed algorithms for decoding.

    Returns:
    dict: The decoded payload of the JWT token.

    Raises:
    HTTPException: If the token is invalid or expired.
    """
    try:
        payload = decode(token, secret_key, algorithms=algorithms)
        return payload
    except (DecodeError, ExpiredSignatureError):
        raise HTTPException(
            detail="Invalid Token!", status_code=status.HTTP_401_UNAUTHORIZED
        )
