import os
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Car Rental Platform"
    API_V1_STR: str = "/api/v1"
    
    # DATABASE
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("DB_HOST", "db")
    POSTGRES_PORT: str = os.getenv("DB_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "car_rental")
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # SECURITY
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:80",
        "http://localhost",
        "https://nova-car-hire-frontend.vercel.app",
        "https://nova-drive.fly.dev" 
    ]

    @field_validator("DATABASE_URL")
    @classmethod
    def assemble_db_connection(cls, v: str | None) -> str | None:
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    class Config:
        case_sensitive = True

settings = Settings()
