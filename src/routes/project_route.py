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
from src.utils.types import CreateProject
from src.utils.index import is_valid_uuid
from src.services.project_service import (
    create_project,
    get_all_projects_with_pagination,
)
from src.middlewares.validate_file_middleware import validate_file
from src.middlewares.authentication_middleware import verify_auth_token

router = APIRouter(tags=["Projects"])

AuthMiddleWare = Annotated[str, Depends(verify_auth_token)]
ValidateFileMiddleWare = Annotated[File, Depends(validate_file)]


@router.post(
    API_ENDPOINTS["PROJECTS"]["CREATE_PROJECT"],
    description="Create Project API",
    # response_model=LoginRespose,
)
def add_project(body: CreateProject, response: Response):
    """
    Endpoint for create new project.

    Parameters:
    - body (): New project details.
    - response (Response): FastAPI Response object.

    Returns:
    ProjectResponse: The project response.

    Raises:
    - SQLAlchemyError: If there is an error in the database operation.
    - Exception: For unexpected errors during create new project.
    """
    return create_project(body, response)


@router.get(
    API_ENDPOINTS["PROJECTS"]["GET_ALL_PROJECTS"],
    description="Get all Projects API",
    # response_model=LoginRespose,
)
def get_all_users(
    _: AuthMiddleWare,
    response: Response,
    page: int = 1,
    page_size: int = 10,
):
    """
    Endpoint for create new project.

    Parameters:
    - body (): New project details.
    - response (Response): FastAPI Response object.

    Returns:
    ProjectResponse: The project response.

    Raises:
    - SQLAlchemyError: If there is an error in the database operation.
    - Exception: For unexpected errors during create new project.
    """
    return get_all_projects_with_pagination(response, page, page_size)
