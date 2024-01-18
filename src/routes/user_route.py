from fastapi import APIRouter, Response, Depends, HTTPException
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
    get_all_users_with_pagination,
    get_user_info_by_id,
)
from src.middlewares.authentication_middleware import verify_auth_token

router = APIRouter(tags=["Users"])

@router.post(
    API_ENDPOINTS["USERS"]["REGISTER"],
    description="Register Account API",
    response_model=RegisterResponse,
)
def register_user(body: RegisterUser, response: Response) -> RegisterResponse:
    """
    Endpoint for registering a new user.

    Parameters:
    - body (RegisterUser): The registration details.
    - response (Response): FastAPI Response object.

    Returns:
    RegisterResponse: The registration response.

    Raises:
    - DatabaseException: If there is an error in the database operation.
    """
    return create_account(body, response)

@router.post(
    API_ENDPOINTS["USERS"]["LOGIN"],
    description="Login User API",
    response_model=LoginResponse,
)
def login_user(body: LoginUser, response: Response) -> LoginResponse:
    """
    Endpoint for user authentication.

    Parameters:
    - body (LoginUser): The login details.
    - response (Response): FastAPI Response object.

    Returns:
    LoginResponse: The login response.

    Raises:
    - SQLAlchemyError: If there is an error in the database operation.
    - Exception: For unexpected errors during user authentication.
    """
    return authenticate_user(body, response)

CommonsDep = Annotated[str, Depends(verify_auth_token)]

@router.get(
    API_ENDPOINTS["USERS"]["WHO_AM_I"], description="Fetch Who Am I information",
    response_model=WhoAMIResponse,
)
def who_am_i(userInfo: CommonsDep) -> WhoAMIResponse:
    """
    Endpoint for fetching user information.

    Parameters:
    - userInfo (CommonsDep): User information.

    Returns:
    WhoAMIResponse: User information response.

    Raises:
    - HTTPException: If there is an HTTP-related exception.
    """
    try:
        return {"success": True, "data": userInfo}
    except HTTPException as error:
        return error.detail

@router.get(
    API_ENDPOINTS["USERS"]["USER_BY_ID"], description="Get User By ID",
    response_model=WhoAMIResponse,
)
def get_user_by_id(user_id: str, _: CommonsDep, response: Response) -> WhoAMIResponse:
    """
    Endpoint for fetching user information by ID.

    Parameters:
    - user_id (str): User ID.
    - _: CommonsDep: Dependency for verifying authentication.
    - response (Response): FastAPI Response object.

    Returns:
    WhoAMIResponse: User information response.

    Raises:
    - SQLAlchemyError: If there is an error in the database operation.
    """
    return get_user_info_by_id(user_id, response)

@router.get(
    API_ENDPOINTS["USERS"]["GET_ALL_USERS"], description="Get All Users",
    response_model=GetAllUsers,
)
def get_all_users(
    _: CommonsDep,
    response: Response,
    page: int = 1,
    page_size: int = 10,
) -> GetAllUsers:
    """
    Endpoint for fetching all users with pagination.

    Parameters:
    - _: CommonsDep: Dependency for verifying authentication.
    - response (Response): FastAPI Response object.
    - page (int): Page number (default: 1).
    - page_size (int): Number of items per page (default: 10).

    Returns:
    GetAllUsers: Response containing the list of users.

    Raises:
    - NoResultFound: If no users are found.
    - SQLAlchemyError: If there is an error in the database operation.
    """
    return get_all_users_with_pagination(response, page, page_size)
