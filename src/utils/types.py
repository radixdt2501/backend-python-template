from enum import Enum as PythonEnum
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RolesEnum(str, PythonEnum):
    """
    Enumeration for user roles.

    Possible values:
    - ADMIN: Administrator
    - USER: Regular user
    - SUPER_USER: Super user with elevated privileges
    """

    ADMIN = "ADMIN"
    USER = "USER"
    SUPER_USER = "SUPER_USER"


class RegisterUser(BaseModel):
    """
    Model for user registration data.

    Attributes:
    - firstName (str): First name of the user.
    - lastName (Optional[str]): Last name of the user (optional).
    - username (str): Username of the user.
    - email (str): Email address of the user.
    - password (str): Password for user authentication.
    - role (Optional[RolesEnum]): User role (default: USER).
    """

    firstName: str
    lastName: Optional[str] = None
    username: str
    email: str
    password: str
    role: Optional[RolesEnum] = RolesEnum.USER


class LoginUser(BaseModel):
    """
    Model for user login data.

    Attributes:
    - identifier (str): User identifier (username or email).
    - password (str): Password for user authentication.
    """

    identifier: str
    password: str


class LoginResponse(BaseModel):
    """
    Model for the response after a user login.

    Attributes:
    - message (str): Response message.
    - success (bool): Indicates whether the login was successful.
    - token (Optional[str]): JWT token (optional).
    """

    message: str
    success: bool
    token: Optional[str]


class BaseSuccessResponse(BaseModel):
    """
    Model for the response after a user registration.

    Attributes:
    - message (str): Response message.
    - success (bool): Indicates whether the registration was successful.
    - id (Optional[str]): User ID (optional).
    """

    message: str
    success: bool
    id: Optional[str]


class UserInfo(BaseModel):
    """
    Model for basic user information.

    Attributes:
    - id (str): User ID.
    - email (str): Email address of the user.
    - first_name (str): First name of the user.
    - last_name (str): Last name of the user.
    - username (str): Username of the user.
    - role (str): User role.
    """

    id: str
    email: str
    first_name: str
    last_name: str
    username: str
    role: RolesEnum


class WhoAMIResponse(BaseModel):
    """
    Model for the response after querying user information.

    Attributes:
    - success (bool): Indicates whether the query was successful.
    - data (Optional[UserInfo]): User information (optional).
    """

    success: bool
    data: Optional[UserInfo]


class UserInfoExtended(BaseModel):
    """
    Model for extended user information.

    Attributes:
    - id (str): User ID.
    - first_name (str): First name of the user.
    - last_name (str): Last name of the user.
    - username (str): Username of the user.
    - email (str): Email address of the user.
    - role (str): User role.
    - is_verified (bool): Indicates whether the user is verified.
    - is_deleted (bool): Indicates whether the user is deleted.
    - created_at (datetime): Timestamp of user creation.
    - updated_at (datetime): Timestamp of last user update.
    """

    id: str
    first_name: str
    last_name: Optional[str] = None
    username: str
    email: str
    role: RolesEnum
    profile_picture_path: Optional[str] = None
    is_verified: bool
    is_deleted: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GetAllUsers(BaseModel):
    """
    Model for the response after querying all users.

    Attributes:
    - success (bool): Indicates whether the query was successful.
    - data (List[UserInfoExtended]): List of extended user information.
    """

    success: bool
    data: List[UserInfoExtended]
