from datetime import datetime
from enum import Enum as PythonEnum
from typing import List, Optional

from pydantic import UUID4, BaseModel


class ProjectStatusEnum(str, PythonEnum):
    """
    Enumeration for user roles.

    Possible values:
    - OPEN: Open
    - UPCOMING: Upcoming
    - IN_PROGRESS: In Progress
    - CLOSED: Closed
    """

    OPEN = "OPEN"
    UPCOMING = "UPCOMING"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class CreateProjectDetails(BaseModel):
    name: str
    description: str
    city: str
    country: str
    start_date: datetime
    end_date: datetime


class CreateProjectMembers(BaseModel):
    email_ids: List[str]


class ProjectInfoExtended(BaseModel):
    id: UUID4
    name: str
    description: str
    city: str
    country: str
    start_date: datetime
    end_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    project_owner_id: UUID4
    project_members_id: UUID4
    project_members_email_ids: List[str]
    owner_first_name: str
    owner_last_name: str


class GetAllProjectsResponse(BaseModel):
    success: bool
    data: List[ProjectInfoExtended]
