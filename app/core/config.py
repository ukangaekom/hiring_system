from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hiring System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkeyneedschange"  # TODO: Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    # Database
    DATABASE_URL: str = "postgresql://app_user:app_password@localhost:5432/edu_pro"
    
    # Uploads
    UPLOAD_DIR: str = "uploads"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
