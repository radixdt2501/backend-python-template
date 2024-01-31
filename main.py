from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.config.database.db_connection import get_db
from src.routes import user_route, project_route
from utils.constants import API_ENDPOINTS

# Load environment variables from the specified file
load_dotenv(dotenv_path="src/config/env-files/.env.local")

# Create a FastAPI instance
app = FastAPI()

def get_db_session() -> Session:
    """
    Dependency function to provide a database session for route operations.

    Returns:
        Session: SQLAlchemy database session
    """
    db = get_db()
    try:
        yield db
    finally:
        db.close()

# Include user routes with a specified prefix and tags
app.include_router(
    user_route.router, prefix=API_ENDPOINTS["USERS"]["BASE_URL"], tags=["Users"]
)
app.include_router(
    project_route.router, prefix=API_ENDPOINTS["PROJECTS"]["BASE_URL"], tags=["Projects"]
)

# Additional FastAPI configurations (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def read_root(db: Session = Depends(get_db_session)) -> dict:
    """
    Endpoint to check the health of the application.

    Parameters:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db_session).

    Returns:
        dict: Health status
    """
    # Your logic using the database session goes here
    return {"health": True}