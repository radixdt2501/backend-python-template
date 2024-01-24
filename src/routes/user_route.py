from fastapi import (
    APIRouter,
    File,
    Form,
    Response,
    Depends,
    HTTPException,
    UploadFile,
)
from typing import Annotated

from src.utils.constants import API_ENDPOINTS
from src.utils.types import (
    GetAllUsers,
    RegisterUser,
    BaseSuccessResponse,
    LoginUser,
    LoginResponse,
    RolesEnum,
    UserInfoExtended,
    WhoAMIResponse,
)
from src.utils.index import is_valid_uuid
from src.services.user_service import (
    create_account,
    authenticate_user,
    get_all_users_with_pagination,
    get_user_info_by_id,
    update_user_with_image,
)
from src.middlewares.validate_file_middleware import validate_file
from src.middlewares.authentication_middleware import verify_auth_token

router = APIRouter(tags=["Users"])

AuthMiddleWare = Annotated[str, Depends(verify_auth_token)]
ValidateFileMiddleWare = Annotated[File, Depends(validate_file)]


@router.post(
    API_ENDPOINTS["USERS"]["REGISTER"],
    description="Register Account API",
    response_model=BaseSuccessResponse,
)
def register_user(body: RegisterUser, response: Response) -> BaseSuccessResponse:
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


@router.get(
    API_ENDPOINTS["USERS"]["WHO_AM_I"],
    description="Fetch Who Am I information",
    response_model=WhoAMIResponse,
)
def who_am_i(userInfo: AuthMiddleWare) -> WhoAMIResponse:
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
    API_ENDPOINTS["USERS"]["USER_BY_ID"],
    description="Get User By ID",
    response_model=WhoAMIResponse,
)
def get_user_by_id(
    user_id: str, _: AuthMiddleWare, response: Response
) -> WhoAMIResponse:
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
    API_ENDPOINTS["USERS"]["GET_ALL_USERS"],
    description="Get All Users",
    response_model=GetAllUsers,
)
def get_all_users(
    _: AuthMiddleWare,
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


@router.put(
    API_ENDPOINTS["USERS"]["USER_BY_ID"],
    description="Update User Information with Profile Picture Image",
    response_model=BaseSuccessResponse,
)
async def update_user(
    user_id: str,
    __: AuthMiddleWare,
    ___: ValidateFileMiddleWare,
    response: Response,
    file: Annotated[UploadFile, File()] = None,
    first_name: Annotated[str, Form()] = None,
    last_name: Annotated[str, Form()] = None,
    username: Annotated[str, Form()] = None,
    email: Annotated[str, Form()] = None,
    role: Annotated[RolesEnum, Form()] = None,
    is_verified: Annotated[bool, Form()] = False,
    is_deleted: Annotated[bool, Form()] = False,
) -> BaseSuccessResponse:
    """
    Update user information along with the profile picture.

    Parameters:
    - _: AuthMiddleWare: Custom authentication middleware.
    - __: ValidateFileMiddleWare: Custom file validation middleware.
    - response (Response): FastAPI Response object.
    - user_id (str): User ID to update.
    - file: Annotated[UploadFile, File()]: Uploaded profile picture file.
    - first_name (Annotated[str, Form()]): First name of the user.
    - last_name (Annotated[str, Form()]): Last name of the user.
    - username (Annotated[str, Form()]): Username of the user.
    - email (Annotated[str, Form()]): Email of the user.
    - role (Annotated[RolesEnum, Form()]): Role of the user.
    - is_verified (Annotated[bool, Form()]): Verification status of the user.
    - is_deleted (Annotated[bool, Form()]): Deletion status of the user.

    Returns:
    Dict[str, any]: Dictionary containing the success status, message, and user ID if successful.

    Raises:
    IntegrityError: If there is an integrity violation (e.g., unique constraint).
    SQLAlchemyError: If there is an error in the database operation.
    """
    is_valid_uuid(user_id)
    profile_picture_path = f"/uploads/{file.filename}" if file else None

    payload: UserInfoExtended = {
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "role": role,
        "is_verified": is_verified,
        "is_deleted": is_deleted,
        "profile_picture": profile_picture_path,
    }
    return update_user_with_image(response, payload, file)
