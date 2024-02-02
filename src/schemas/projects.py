from datetime import datetime
from enum import Enum as PythonEnum
from typing import List, Optional

from pydantic import BaseModel


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