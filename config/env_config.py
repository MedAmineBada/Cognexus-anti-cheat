from pydantic_settings import BaseSettings


class EnvFile(BaseSettings):

    class Config:
        env_file = ".env"


env = EnvFile()
