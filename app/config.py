from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application & secret config (loaded from .env)."""
    # LinkedIn
    linkedin_client_id: str = Field(..., env="LINKEDIN_CLIENT_ID")
    linkedin_client_secret: str = Field(..., env="LINKEDIN_CLIENT_SECRET")
    linkedin_redirect_uri: str = Field("http://localhost:8000/callback", env="LINKEDIN_REDIRECT_URI")

    # LLM
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    llm_model: str = Field("gpt-4o", env="CREWAI_MODEL")

    # Infra
    database_url: str = Field("postgresql+psycopg2://leadgen:pass@localhost/leadgen", env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    class Config:
        env_file = ".env"

settings = Settings()