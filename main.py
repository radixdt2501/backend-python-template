import os
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.middlewares.authentication_middleware import verify_auth_token
from src.config.database.db_connection import get_db
from src.routes import user_route, project_route
from src.utils.constants import API_ENDPOINTS, UPLOADS_FOLDER_PATH

# Load environment variables from the specified file
load_dotenv(dotenv_path="src/config/env-files/.env.local")


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


if not os.path.exists(UPLOADS_FOLDER_PATH):
    os.makedirs(UPLOADS_FOLDER_PATH)

# Create a FastAPI instance
app = FastAPI()
AuthMiddleWare = Annotated[str, Depends(verify_auth_token)]

# Include user routes with a specified prefix and tags
app.include_router(
    user_route.router, prefix=API_ENDPOINTS["USERS"]["BASE_URL"], tags=["Users"]
)
app.include_router(
    project_route.router,
    prefix=API_ENDPOINTS["PROJECTS"]["BASE_URL"],
    tags=["Projects"],
)

# Additional FastAPI configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/" + UPLOADS_FOLDER_PATH,
    StaticFiles(directory=UPLOADS_FOLDER_PATH),
    name=UPLOADS_FOLDER_PATH,
)


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get(API_ENDPOINTS["HEALTH"])
def read_root(db: Session = Depends(get_db_session)) -> dict:
    """
    Endpoint to check the health of the application.
    Returns:
        dict: Health status
    """
    return {"health": True}


@app.get(API_ENDPOINTS["FILES"])
async def retrive_file_by_file_path(file_path: str):
    file_name = file_path.split("/")[1].split("_")[1]
    return FileResponse(
        file_path, media_type="application/octet-stream", filename=file_name
    )
