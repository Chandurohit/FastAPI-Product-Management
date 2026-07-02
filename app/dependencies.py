from typing import Generator
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.core.config import settings
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user_model import User

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session.
    Automatically closes the session after request lifecycle completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Dependency that reads JWT from the HttpOnly cookie, validates claims,
    and returns the authenticated user from the database.
    """
    # Retrieve cookie from request
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Decode and validate signature/exp/iss/aud
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication session"
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token identity payload mismatch"
        )
    
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
        
    return user
