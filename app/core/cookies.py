from fastapi import Response
from app.core.config import settings

def set_auth_cookie(response: Response, token: str):
    """
    Sets the secure JWT auth cookie with HttpOnly, SameSite=Lax/Strict configuration.
    """
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite=settings.COOKIE_SAMESITE,
        secure=settings.COOKIE_SECURE,
        path="/"
    )

def clear_auth_cookie(response: Response):
    """
    Clears the auth cookie by deleting it from the client.
    """
    response.delete_cookie(
        key=settings.COOKIE_NAME,
        path="/",
        httponly=True,
        samesite=settings.COOKIE_SAMESITE,
        secure=settings.COOKIE_SECURE
    )
