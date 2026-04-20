from pydantic_settings import BaseSettings


class EnvFile(BaseSettings):
    MODEL: str
    HFTOKEN: str

    QDRANT_HOST: str
    QDRANT_PORT: int
    VECTOR_SIZE: int
    SIMILARITY_THRESHOLD: float

    class Config:
        env_file = ".env"


env = EnvFile()
