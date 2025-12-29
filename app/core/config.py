from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MCP-Guard"
    DATABASE_URL: str
    GOOGLE_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENV: str

    class Config:
        env_file = ".env"

settings = Settings()
