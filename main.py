from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.config.database.db_connection import get_db
from src.routes import user_route
from utils.constants import API_ENDPOINTS


def get_db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
load_dotenv(dotenv_path="src/config/env-files/.env.local")

# Include your route modules
app.include_router(
    user_route.router, prefix=API_ENDPOINTS["USERS"]["BASE_URL"], tags=["Users"]
)
# app.include_router(project_route.router, prefix="/projects", tags=["projects"])

# Additional FastAPI configurations (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def read_root(db: Session = Depends(get_db_session)):
    # Your logic using the database session
    return {"health": True}
