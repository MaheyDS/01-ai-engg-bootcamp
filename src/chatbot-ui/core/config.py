from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    openai_api_key: str
    groq_api_key: str
    google_api_key: str
    qdrant_url: str
    qdrant_collection_name: str
    embedding_model: str
    embedding_provider: str

    model_config = SettingsConfigDict(env_file=".env")

config = Config()