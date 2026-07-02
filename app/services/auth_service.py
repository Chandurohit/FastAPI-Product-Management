from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user_model import User

class AuthService:
    @staticmethod
    def register_user(db: Session, username: str, email: str, password: str) -> User:
        """
        Validates uniqueness of email and username, hashes password, and saves the new user.
        """
        # Validate duplicate email
        existing_email = UserRepository.get_by_email(db, email)
        if existing_email:
            raise ValueError("Email is already registered.")

        # Validate duplicate username
        existing_username = UserRepository.get_by_username(db, username)
        if existing_username:
            raise ValueError("Username is already taken.")

        # Hash password and create user
        hashed_password = hash_password(password)
        return UserRepository.create(db, username, email, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> tuple[User, str]:
        """
        Authenticates a user, updates their last login, and generates a JWT access token.
        """
        # Retrieve user by email
        user = UserRepository.get_by_email(db, email)
        if not user:
            raise ValueError("Invalid email or password.")

        # Verify password hash
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password.")

        # Update last login time
        user = UserRepository.update_last_login(db, user.id)

        # Generate access token
        token = create_access_token(user_id=user.id, username=user.username)
        return user, token
