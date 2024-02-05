from typing import Any
from datetime import datetime
from sqlalchemy import Column, DateTime, String, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship, mapped_column

from src.config.database.db_connection import Base
from src.models.project_model import ProjectModel


class Utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(Utcnow, "postgresql")
def pg_utcnow(element: Any, compiler: Any, **kw: Any) -> Any:
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class ProjectDocumentsModel(Base):
    """
    SQLAlchemy model for the 'project_documents' table.
    """

    __tablename__ = "project_documents"

    class Config:
        orm_mode = True

    id = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=text("(gen_random_uuid())"),
    )
    document_path = Column(String, nullable=False)
    project_id = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"))
    project = relationship("ProjectModel", back_populates="project_documents")

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
