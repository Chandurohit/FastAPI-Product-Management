from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.user_model import User

class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> User:
        """
        Retrieves a user by their UUID.
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User:
        """
        Retrieves a user by their email address (case-insensitive).
        """
        return db.query(User).filter(func.lower(User.email) == func.lower(email)).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> User:
        """
        Retrieves a user by their username (case-insensitive).
        """
        return db.query(User).filter(func.lower(User.username) == func.lower(username)).first()

    @staticmethod
    def create(db: Session, username: str, email: str, hashed_password: str) -> User:
        """
        Creates a new user record in the database.
        """
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_last_login(db: Session, user_id: str) -> User:
        """
        Updates the last login timestamp for the specified user.
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.last_login = func.now()
            db.commit()
            db.refresh(db_user)
        return db_user
