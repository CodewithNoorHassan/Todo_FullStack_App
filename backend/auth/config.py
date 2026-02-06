from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    BETTER_AUTH_SECRET: str
    # Keep a `secret_key` attribute for compatibility with other code
    secret_key: str | None = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = "../.env"  # Path from auth directory to main .env file
        env_file_encoding = "utf-8"

    def __init__(self, **values):
        super().__init__(**values)
        # Default secret_key to BETTER_AUTH_SECRET when not provided explicitly
        if not getattr(self, "secret_key", None):
            self.secret_key = self.BETTER_AUTH_SECRET


# Create an instance of the auth settings
auth_settings = AuthSettings()