from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.user_schema import RegisterRequest, LoginRequest, UserResponse, ApiResponse, AuthResponse
from app.services.auth_service import AuthService
from app.core.cookies import set_auth_cookie, clear_auth_cookie
from app.models.user_model import User

router = APIRouter()

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registers a new user account. Returns UserResponse on success.
    """
    try:
        user = AuthService.register_user(db, req.username, req.email, req.password)
        user_resp = UserResponse.model_validate(user)
        return {
            "success": True,
            "message": "User registered successfully.",
            "data": {"user": user_resp}
        }
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": str(e)
            }
        )

@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(req: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """
    Authenticates user, sets HttpOnly auth cookie, and returns user info.
    """
    try:
        user, token = AuthService.authenticate_user(db, req.email, req.password)
        set_auth_cookie(response, token)
        user_resp = UserResponse.model_validate(user)
        return {
            "success": True,
            "message": "Login successful.",
            "data": {"user": user_resp}
        }
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": str(e)
            }
        )

@router.post("/logout", response_model=ApiResponse, status_code=status.HTTP_200_OK)
def logout(response: Response):
    """
    Clears the HttpOnly auth cookie to log out the user.
    """
    clear_auth_cookie(response)
    return {
        "success": True,
        "message": "Logout successful.",
        "data": None
    }

@router.get("/me", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns the profile info of the currently logged-in user.
    """
    user_resp = UserResponse.model_validate(current_user)
    return {
        "success": True,
        "message": "User profile retrieved successfully.",
        "data": {"user": user_resp}
    }
