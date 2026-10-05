from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./recruit.db" # Default fallback for local testing
    environment: str = "production"
    cors_origins: list[str] = ["*"]
    secret_key: str = "change-me"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
