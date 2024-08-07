import uuid

import asyncpg
import psycopg2

from src.infrastructure.db.postgres.interfaces import PostgresSkuRepositoryInterface
from src.infrastructure.db.postgres.settings import get_postgres_settings


class PostgresSkuRepositoryImplement(PostgresSkuRepositoryInterface):
    def __init__(self) -> None:
        self.settings = get_postgres_settings()

    async def upload_data(self, data: dict) -> None:
        conn = await self.settings.get_async_postgres_connect()
        async with conn.transaction():
            await conn.execute(
                """
                
                """,

            )