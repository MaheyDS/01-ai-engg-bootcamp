from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    openai_api_key: str
    groq_api_key: str
    google_api_key: str
    qdrant_url: str
    qdrant_collection_name: str
    embedding_model: str
    embedding_model_provider: str
    generation_model: str
    generation_model_provider: str
    langsmith_tracing: str
    langsmith_endpoint: str
    langsmith_api_key: str
    langsmith_project: str

    model_config = SettingsConfigDict(env_file=".env")

config = Config()