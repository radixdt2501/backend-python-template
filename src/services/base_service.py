from sqlalchemy.orm import Session

class BaseService:
    def __init__(self, db: Session):
        self.db = db

    # You can include other common methods or logic applicable to services
    # For example, methods for CRUD operations on models, etc.
