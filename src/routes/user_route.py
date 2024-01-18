from fastapi import APIRouter, HTTPException, Response, Depends
from typing import Annotated

from src.utils.constants import API_ENDPOINTS
from src.utils.types import (
    GetAllUsers,
    RegisterUser,
    RegisterResponse,
    LoginUser,
    LoginResponse,
    WhoAMIResponse,
)
from src.services.user_service import (
    create_account,
    authenticate_user,
    getAllUsersWithPagination,
    getUserInfoByID,
)
from src.middlewares.authentication_middleware import verify_auth_token

router = APIRouter(tags=["Users"])


@router.post(
    API_ENDPOINTS["USERS"]["REGISTER"],
    description="Register Account API",
)
def register(body: RegisterUser, response: Response) -> RegisterResponse:
    return create_account(body, response)


@router.post(
    API_ENDPOINTS["USERS"]["LOGIN"],
    description="Login User API",
    responses={200: {"identifier": "string", "password": "string"}},
)
def login(
    body: LoginUser,
    response: Response,
) -> LoginResponse:
    return authenticate_user(body, response)


CommonsDep = Annotated[str, Depends(verify_auth_token)]


@router.get(
    API_ENDPOINTS["USERS"]["WHO_AM_I"], description="Fetch Who Am I information"
)
def whoami(userInfo: CommonsDep) -> WhoAMIResponse:
    try:
        return {"success": True, "data": userInfo}
    except HTTPException as error:
        return error.detail


@router.get(API_ENDPOINTS["USERS"]["USER_BY_ID"], description="Get User By ID")
def getUserByID(userId: str, _: CommonsDep, response: Response) -> WhoAMIResponse:
    return getUserInfoByID(userId, response)


@router.get(API_ENDPOINTS["USERS"]["GET_ALL_USERS"], description="Get All Users")
def getAllUsers(
    _: CommonsDep,
    response: Response,
    page: int = 1,
    pageSize: int = 10,
) -> GetAllUsers:
    return getAllUsersWithPagination(response, page, page_size=pageSize)
