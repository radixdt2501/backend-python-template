
from typing import Optional

from pydantic import BaseModel

class BaseSuccessResponse(BaseModel):
    """
    Model for the response after a user registration.

    Attributes:
    - message (str): Response message.
    - success (bool): Indicates whether the registration was successful.
    - id (Optional[str]): User ID (optional).
    """

    message: str
    success: bool
    id: Optional[str]