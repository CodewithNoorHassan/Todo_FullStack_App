from pydantic import BaseSettings
from typing import Optional


class DatabaseSettings(BaseSettings):
    NEON_DATABASE_URL: Optional[str] = None
    DATABASE_URL: str = "sqlite:///./todoapp.db"  # fallback

    class Config:
        env_file = "../.env"  # Path from database directory to main .env
        env_file_encoding = "utf-8"

    def __init__(self, **values):
        super().__init__(**values)
        # If NEON_DATABASE_URL is provided, use it as priority
        if self.NEON_DATABASE_URL:
            self.DATABASE_URL = self.NEON_DATABASE_URL


# Create an instance of the settings
db_settings = DatabaseSettings()