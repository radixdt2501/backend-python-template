from typing import Annotated

from fastapi import APIRouter, Depends, File, Response, UploadFile

from src.middlewares.authentication_middleware import verify_auth_token
from src.middlewares.validate_file_middleware import validate_file

from src.services.project_service import (
    create_project,
    add_project_members,
    fetch_project_member_by_project_id,
    create_project_documents_by_project_id,
    get_all_projects_with_pagination,
)
from src.utils.constants import API_ENDPOINTS

from src.schemas.index import BaseSuccessResponse
from schemas.projects_schema import (
    CreateProjectDetails,
    CreateProjectMembers,
    GetAllProjectsResponse,
)
from utils.index import is_valid_uuid

router = APIRouter(tags=["Projects"])

AuthMiddleWare = Annotated[str, Depends(verify_auth_token)]
ValidateFileMiddleWare = Annotated[File, Depends(validate_file)]


@router.post(
    API_ENDPOINTS["PROJECTS"]["DETAILS"],
    description="Create Project Details API",
    response_model=BaseSuccessResponse,
)
def create_project_details(
    user: AuthMiddleWare, body: CreateProjectDetails, response: Response
) -> BaseSuccessResponse:
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
    response_model=BaseSuccessResponse,
)
def create_project_members(
    _: AuthMiddleWare, project_id: str, body: CreateProjectMembers, response: Response
) -> BaseSuccessResponse:
    is_valid_uuid(project_id)
    return add_project_members(project_id, body, response)


@router.get(
    API_ENDPOINTS["PROJECTS"]["GET_ALL_PROJECTS"],
    description="Fetch all Projects API",
    response_model=GetAllProjectsResponse,
)
def get_all_projects(
    user: AuthMiddleWare,
    response: Response,
    page: int = 1,
    page_size: int = 10,
) -> GetAllProjectsResponse:
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


@router.get(
    API_ENDPOINTS["PROJECTS"]["MEMBERS"],
    description="Fetch Project Members By Project ID API",
    # response_model=GetAllProjectsResponse,
)
def fetch_project_members(
    project_id: str,
    user: AuthMiddleWare,
    response: Response,
):
    is_valid_uuid(project_id)
    return fetch_project_member_by_project_id(
        project_id,
        user,
        response,
    )


@router.post(
    API_ENDPOINTS["PROJECTS"]["DOCUMENTS"],
    description="Add Project Documents in Project API",
    # response_model=GetAllProjectsResponse,
)
def create_project_documents(
    __: AuthMiddleWare,
    project_id: str,
    response: Response,
    file: Annotated[UploadFile, File()] = None,
):
    is_valid_uuid(project_id)
    documents = f"/uploads/{file.filename}" if file else None

    return create_project_documents_by_project_id()
