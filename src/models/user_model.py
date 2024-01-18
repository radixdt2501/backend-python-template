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
    __tablename__ = "users"

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
    role = Column(
        Enum(RolesEnum),
        default=RolesEnum.USER,
        server_default=RolesEnum.USER,
        nullable=False,
    )
    is_verified = Column(Boolean, default=False, nullable=False, server_default="false")
    is_deleted = Column(Boolean, default=False, nullable=False, server_default="false")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=Utcnow(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=Utcnow(),
        onupdate=Utcnow(),
        server_onupdate=Utcnow(),
    )


users_index = Index("users_index", UserModel.first_name, UserModel.last_name)
