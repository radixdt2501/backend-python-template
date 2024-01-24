from sqlalchemy import Column, String, Boolean, DateTime, text, Enum, Index
from sqlalchemy.sql import expression
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression

from typing import Any

from src.config.database.db_connection import Base
from src.utils.types import RolesEnum


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

    id = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=text("(gen_random_uuid())"),
        doc="User ID",
    )
    first_name = Column(String, index=True, nullable=False, doc="User's first name")
    last_name = Column(String, index=True, nullable=True, doc="User's last name")
    username = Column(String, unique=True, index=True, nullable=False, doc="Unique username")
    email = Column(String, unique=True, index=True, nullable=False, doc="User's email address")
    password = Column(String, nullable=False, doc="User's hashed password")
    profile_picture = Column(String, nullable=True, doc="User's Profile Picture URL")
    role = Column(
        Enum(RolesEnum),
        default=RolesEnum.USER,
        server_default=RolesEnum.USER,
        nullable=False,
        doc="User's role (enum)",
    )
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        server_default="false",
        doc="Indicates if the user is verified",
    )
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        server_default="false",
        doc="Indicates if the user is deleted",
    )
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
        # onupdate=Utcnow(),
        # server_onupdate=Utcnow(),
        doc="Timestamp of user last update",
    )


# Updated index name for better clarity
users_name_index = Index("users_name_index", UserModel.first_name, UserModel.last_name)
