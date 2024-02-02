# src/config/database/seeders/seed.py
from sqlalchemy.orm import sessionmaker

from src.config.database.db_connection import engine
from src.services.user_service import create_account
from schemas.users_schema import RegisterUser


def seed_users():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Your seeding logic here
    users_to_seed = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "john_doe",
            "email": "john.doe@example.com",
            "password": "password1",
            "role": "user",  # Add the role field for each user
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "username": "jane_smith",
            "email": "jane.smith@example.com",
            "password": "password2",
            "role": "user",
        },
    ]

    for user_data in users_to_seed:
        payload = RegisterUser(**user_data)
        try:
            create_account(payload, db)
        except Exception as e:
            print(f"Error seeding user: {e}")

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_users()
