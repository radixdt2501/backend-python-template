import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from src.utils.index import get_required_env_variable

# Load environment variables
load_dotenv(dotenv_path="src/config/env-files/.env.local")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Load required environment variables
POSTGRES_DB_NAME = get_required_env_variable("POSTGRES_DB_NAME")
POSTGRES_USERNAME = get_required_env_variable("POSTGRES_USERNAME")
POSTGRES_PASSWORD = get_required_env_variable("POSTGRES_PASSWORD")
POSTGRES_HOST = get_required_env_variable("POSTGRES_HOST")
POSTGRES_PORT = get_required_env_variable("POSTGRES_PORT")

# Database URL format for SQLAlchemy
DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
session = Session(engine)

# Log database connection status
try:
    # Try to establish a connection
    with engine.connect() as connection:
        logger.info("Database connection successful")

except (Exception, SQLAlchemyError) as error:
    # Log any errors
    logger.error(f"Database connection error: {error}")

# Create a SessionLocal class to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

# Function to get a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
