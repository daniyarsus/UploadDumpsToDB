import datetime

import asyncpg

from src.infrastructure.db.postgres.interfaces import PostgresMarketplacesRepositoryInterface
from src.infrastructure.db.postgres.dto import PostgresMarketplacesUploadDataDTO
from src.infrastructure.db.postgres.settings import get_postgres_settings


class PostgresMarketplacesRepositoryImplement(PostgresMarketplacesRepositoryInterface):
    async def insert_data(
            self,
            dto: PostgresMarketplacesUploadDataDTO
    ) -> None:
        conn = await get_postgres_settings().get_async_postgres_connect()
        try:
            async with conn.transaction():
                await conn.execute(
                    """
                    INSERT INTO public.marketplaces (
                        name,
                        logo,
                        base_url,
                        src,
                        last_lookup
                    )
                    VALUES (
                        $1,
                        $2,
                        $3,
                        $4,
                        $5
                    )
                    """,
                    dto.name,
                    dto.logo,
                    dto.base_url,
                    dto.src,
                    datetime.datetime.now()
                )
        finally:
            await conn.close()
