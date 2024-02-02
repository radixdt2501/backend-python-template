from typing import Any

from sqlalchemy import Boolean, Column, DateTime, Enum, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship

from src.config.database.db_connection import Base
from schemas.users_schema import UserRoleEnum

class Utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(Utcnow, "postgresql")
def pg_utcnow(element: Any, compiler: Any, **kw: Any) -> Any:
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class UserModel(Base):
    """
    SQLAlchemy model for the 'users' table.
    """

    __tablename__ = "users"

    class Config:
        orm_mode = True

    id = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=text("(gen_random_uuid())"),
    )
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    role = Column(
        Enum(UserRoleEnum),
        default=UserRoleEnum.USER,
        server_default=UserRoleEnum.USER,
        nullable=False,
    )
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        server_default="false",
    )
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        server_default="false",
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=Utcnow(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=Utcnow(),
    )
    projects = relationship("ProjectModel", back_populates="project_owner")


users_name_index = Index("users_name_index", UserModel.first_name, UserModel.last_name)
