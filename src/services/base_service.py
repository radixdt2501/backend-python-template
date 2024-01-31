from sqlalchemy.orm import Session


class BaseService:
    """
    Base service class for interacting with the database.

    Attributes:
    - db (Session): SQLAlchemy database session.
    """

    def __init__(self, db: Session):
        """
        Initializes the BaseService with a database session.

        Parameters:
        - db (Session): SQLAlchemy database session.
        """
        self.db = db

    # You can include other common methods or logic applicable to services
    # For example, methods for CRUD operations on models, etc.
