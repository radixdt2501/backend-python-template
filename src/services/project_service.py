from fastapi import Response, status
from typing import Dict, List
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError

from src.config.database.db_connection import engine
from src.models.project_model import ProjectModel

from src.models.project_members_model import ProjectMembersModel
from src.utils.exceptions import DatabaseException
from src.schemas.projects import CreateProjectDetails, CreateProjectMembers


def create_project(payload: CreateProjectDetails, response: Response):
    stmt = insert(ProjectModel).values(**payload.model_dump())
    with engine.begin() as conn:
        try:
            result = conn.execute(stmt)
            return {
                "success": True,
                "message": "Project Created Successfully",
                "id": str(result.inserted_primary_key[0]),
            }
        except IntegrityError:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {
                "success": False,
                "message": "Something went wrong while creating project details!",
                "id": None,
            }
        except SQLAlchemyError as error:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise DatabaseException(
                f"Something went wrong in DB while creating project details! {error}"
            ) from error


def create_project_members(
    project_id: str, body: CreateProjectMembers, response: Response
):
    stmt = insert(ProjectMembersModel).values(
        project_id=project_id, email_ids=body.email_ids
    )
    with engine.begin() as conn:
        try:
            result = conn.execute(stmt)
            return {
                "success": True,
                "message": "Project Members Created Successfully",
                "id": str(result.inserted_primary_key[0]),
            }
        except IntegrityError:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {
                "success": False,
                "message": "Something went wrong while creating project members!",
                "id": None,
            }
        except SQLAlchemyError as error:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise DatabaseException(
                f"Something went wrong in DB while creating project members! {error}"
            ) from error


def get_all_projects_with_pagination(
    response: Response, page: int = 1, page_size: int = 10
):
    """
    Retrieve all projects with pagination.

    Parameters:
    - response (Response): FastAPI Response object.
    - page (int): Page number (default: 1).
    - page_size (int): Number of items per page (default: 10).

    Returns:
    dict: Response containing the list of projects.

    Raises:
    - NoResultFound: If no projects are found.
    - SQLAlchemyError: If there is an error in the database operation.
    """
    try:
        skip = (page - 1) * page_size
        query = (
            select(
                ProjectModel,
                ProjectMembersModel.id.label("project_members_id"),
                ProjectMembersModel.email_ids.label("project_members_email_ids"),
            )
            .join(ProjectMembersModel)
            .offset(skip)
            .limit(page_size)
        )

        with engine.begin() as conn:
            result = conn.execute(query)
            projects_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]

            return {"success": True, "data": projects_list}

    except NoResultFound:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise NoResultFound("No projects found") from None

    except SQLAlchemyError as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise SQLAlchemyError(
            f"Error during project retrieval with pagination : {error}"
        ) from error
