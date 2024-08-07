import os

from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


def get_general_settings() -> GeneralSettings:
    return GeneralSettings()
