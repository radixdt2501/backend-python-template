from sqlalchemy import Column, String, DateTime, text, ForeignKey, Index
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles

from typing import Any

from src.config.database.db_connection import Base


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

    id = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=text("(gen_random_uuid())"),
        doc="User ID",
    )
    name = Column(String, index=True, nullable=False)
    project_owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    project_owner = relationship("UserModel")

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=Utcnow(),
        doc="Timestamp of user creation",
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=Utcnow(),
        doc="Timestamp of user last update",
    )


project_index = Index("project_index", ProjectModel.name)
