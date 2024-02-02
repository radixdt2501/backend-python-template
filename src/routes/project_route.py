from typing import Annotated

from fastapi import APIRouter, Depends, File, Response

from src.middlewares.authentication_middleware import verify_auth_token
from src.middlewares.validate_file_middleware import validate_file
from src.services.project_service import (
    create_project,
    create_project_members,
    get_all_projects_with_pagination,
)
from src.utils.constants import API_ENDPOINTS
from src.schemas.projects import CreateProjectDetails, CreateProjectMembers

router = APIRouter(tags=["Projects"])

AuthMiddleWare = Annotated[str, Depends(verify_auth_token)]
ValidateFileMiddleWare = Annotated[File, Depends(validate_file)]


@router.post(
    API_ENDPOINTS["PROJECTS"]["DETAILS"],
    description="Create Project Details API",
    # response_model=LoginRespose,
)
def create_project_details(
    user: AuthMiddleWare, body: CreateProjectDetails, response: Response
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
    return create_project(body, user, response)


@router.post(
    API_ENDPOINTS["PROJECTS"]["MEMBERS"],
    description="Add Project Members in Project API",
)
def create_project_members_by_project_id(
    _: AuthMiddleWare, project_id: str, body: CreateProjectMembers, response: Response
):
    return create_project_members(project_id, body, response)


@router.get(
    API_ENDPOINTS["PROJECTS"]["GET_ALL_PROJECTS"],
    description="Get all Projects API",
)
def get_all_projects(
    user: AuthMiddleWare,
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
    return get_all_projects_with_pagination(response, user, page, page_size)
