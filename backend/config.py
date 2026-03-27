from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"
    claude_max_tokens: int = 8192
    max_file_size_bytes: int = 10 * 1024 * 1024  # 10MB
    access_code: str = ""  # If set, users must enter this to use the app
    access_hint: str = ""  # Question/hint shown on the access code screen
    rate_limit_per_hour: int = 10  # Max requests per IP per hour

    class Config:
        env_file = ".env"


settings = Settings()
