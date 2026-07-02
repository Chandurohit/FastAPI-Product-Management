from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import Self

class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str
    
    SECRET_KEY: str = "dev_default_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    COOKIE_NAME: str = "access_token"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    # Placeholders for future configurations (JWT, Cloudinary, Email, Redis)
    JWT_SECRET_KEY: str = "default_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    
    REDIS_URL: str = "redis://localhost:6379/0"

    @model_validator(mode="after")
    def validate_production_secret(self) -> Self:
        if self.ENV.lower() == "production":
            if not self.SECRET_KEY or self.SECRET_KEY == "dev_default_secret_key_change_in_production":
                raise ValueError("In production, a valid, secure SECRET_KEY must be configured in environment variables.")
        return self

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
