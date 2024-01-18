from enum import Enum as PythonEnum
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RolesEnum(str, PythonEnum):
    ADMIN = "ADMIN"
    USER = "USER"
    SUPER_USER = "SUPER_USER"


class RegisterUser(BaseModel):
    firstName: str
    lastName: Optional[str] = None
    username: str
    email: str
    password: str
    role: Optional[RolesEnum] = RolesEnum.USER


class LoginUser(BaseModel):
    identifier: str
    password: str


class LoginResponse(BaseModel):
    message: str
    success: bool
    token: Optional[str]


class RegisterResponse(BaseModel):
    message: str
    success: bool
    id: Optional[str]

class UserInfo(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    username: str
    role: str
    
class WhoAMIResponse(BaseModel):
    success: bool
    data: Optional[UserInfo]
    
class UserInfoExtended(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    is_verified: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

class GetAllUsers(BaseModel):
    success: bool
    data: List[UserInfoExtended]