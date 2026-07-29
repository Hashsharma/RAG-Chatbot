from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    model_name: str = "BAAI/bge-small-en-v1.5"
    model_cache_dir: str = "./model_cache"
    vector_db_path: str = "./data/chroma_db"

    model_device: str = "cuda"

     # ChromaDB settings
    chroma_db_path: str = "./storage/chroma_db"
    chroma_collection: str = "qna_collections"

    llm_model: str
    llm_api_base: str
    llm_api_key: str
    llm_is_chat_model: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()