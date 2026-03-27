from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"
    claude_max_tokens: int = 8192
    max_file_size_bytes: int = 10 * 1024 * 1024  # 10MB
    max_cost_per_request: float = 0.25  # Max cost in USD per request
    access_code: str = ""  # If set, users must enter this to use the app
    access_hint: str = ""  # Question/hint shown on the access code screen

    class Config:
        env_file = ".env"


settings = Settings()
