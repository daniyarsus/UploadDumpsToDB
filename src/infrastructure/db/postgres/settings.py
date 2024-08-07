import psycopg2
import asyncpg

from src.settings import get_general_settings


class PostgresSettings:
    def __init__(self) -> None:
        self.POSTGRES_NAME = get_general_settings().POSTGRES_NAME
        self.POSTGRES_USER = get_general_settings().POSTGRES_USER
        self.POSTGRES_PASS = get_general_settings().POSTGRES_PASS
        self.POSTGRES_HOST = get_general_settings().POSTGRES_HOST
        self.POSTGRES_PORT = get_general_settings().POSTGRES_PORT
        self.POSTGRES_DRIVER =  "postgresql"
        self.ASYNC_POSTGRES_DRIVER = "postgresql"

    def get_postgres_uri(self) -> str:
        return (
            f"{self.POSTGRES_DRIVER}://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASS}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_NAME}"
        )

    def get_async_postgres_uri(self) -> str:
        return (
            f"{self.ASYNC_POSTGRES_DRIVER}://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASS}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_NAME}"
        )

    def get_postgres_connect(self) -> object:
        conn = psycopg2.connect(
            self.get_postgres_uri()
        )
        return conn

    async def get_async_postgres_connect(self) -> object:
        conn = await asyncpg.connect(
            self.get_async_postgres_uri()
        )
        return conn


def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()
