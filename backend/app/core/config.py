from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
    ENVIRONMENT: str = Field(..., env="ENVIRONMENT")
    PLATFORM_URL: str = Field(..., env="PLATFORM_URL")

    APP_NAME: str = "InteractiveLabs"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "InteractiveLabs API for using in browser IDE"

    OPENROUTER_API_KEY: str = Field(..., env="OPENROUTER_API_KEY")

    LANGFUSE_PUBLIC_KEY: str = Field(..., env="LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: str = Field(..., env="LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST: str = Field(..., env="LANGFUSE_HOST")

    SLACK_WEBHOOK_URL_HIGH_PRIORITY : str = Field(..., env="SLACK_WEBHOOK_URL_HIGH_PRIORITY")
    SLACK_WEBHOOK_URL_LOW_PRIORITY : str = Field(..., env="SLACK_WEBHOOK_URL_LOW_PRIORITY")


settings = Settings()