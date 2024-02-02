from typing import Any, List
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.orm import mapped_column, relationship

from src.schemas.projects import ProjectStatusEnum
from src.config.database.db_connection import Base
from src.models.user_model import UserModel

class Utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(Utcnow, "postgresql")
def pg_utcnow(element: Any, compiler: Any, **kw: Any) -> Any:
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class ProjectModel(Base):
    """
    SQLAlchemy model for the 'projects' table.
    """

    __tablename__ = "projects"

    class Config:
        orm_mode = True

    id = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=text("(gen_random_uuid())"),
    )
    name: str = Column(String, index=True, nullable=False)
    description: str = Column(String, nullable=False)
    city: str = Column(String, nullable=False)
    country: str = Column(String, nullable=False)
    start_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )
    end_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )
    status = Column(
        Enum(ProjectStatusEnum),
        default=ProjectStatusEnum.UPCOMING,
        server_default=ProjectStatusEnum.UPCOMING,
        nullable=False,
    )
    created_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=Utcnow(),
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=Utcnow(),
    )
    project_members = relationship("ProjectMembersModel", back_populates="project")
    project_owner_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    project_owner = relationship("UserModel", back_populates="projects")


project_index = Index("project_index", ProjectModel.name)
