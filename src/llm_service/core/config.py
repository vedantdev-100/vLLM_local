from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Local LLM Service"
    app_host: str = "0.0.0.0"
    app_port: int = 8080

    vllm_base_url: str = "http://localhost:8000"
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"

    request_timeout: float = 120.0

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()