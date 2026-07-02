from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import uuid
from app.core.config import settings

# Initialize CryptContext for bcrypt password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Generates a secure bcrypt hash of a plaintext password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a bcrypt hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str, username: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a JWT access token containing claims: sub, user_id, exp, iat, iss, aud, jti.
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    claims = {
        "sub": username,
        "user_id": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "iss": "TeluskoTracBackend",
        "aud": "TeluskoTracFrontend",
        "jti": str(uuid.uuid4())
    }
    
    return jwt.encode(claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes and validates a JWT access token.
    Checks signature, expiration (exp), audience (aud), and issuer (iss).
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience="TeluskoTracFrontend",
            issuer="TeluskoTracBackend"
        )
        return payload
    except JWTError:
        return None
