import uuid

import asyncpg
import psycopg2

from src.infrastructure.db.postgres.interfaces import PostgresSkuRepositoryInterface
from src.infrastructure.db.postgres.dto import PostgresSKUUploadDataDTO
from src.infrastructure.db.postgres.settings import get_postgres_settings


class PostgresSkuRepositoryImplement(PostgresSkuRepositoryInterface):
    def __init__(self) -> None:
        self.settings = get_postgres_settings()

    async def upload_data(
            self,
            dto: PostgresSKUUploadDataDTO
    ) -> None:
        conn = await self.settings.get_async_postgres_connect()
        async with conn.transaction():
            await conn.execute(
                '''
                INSERT INTO public.sku(
                    uuid, 
                    marketplace_id, 
                    product_id, 
                    title, 
                    description, 
                    brand, 
                    seller_id, 
                    seller_name, 
                    first_image_url, 
                    category_id, 
                    category_lvl_1, 
                    category_lvl_2, 
                    category_lvl_3, 
                    category_remaining, 
                    features, 
                    rating_count, 
                    rating_value, 
                    price_before_discounts, 
                    discount, 
                    price_after_discounts, 
                    bonuses, 
                    sales, 
                    inserted_at, 
                    updated_at, 
                    currency, 
                    referral_url, 
                    barcode, 
                    original_url, 
                    mpn, 
                    status, 
                    revenue, 
                    images, 
                    last_seen_at
                ) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, 
                          $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, 
                          $29, $30, $31, $32, $33)
                ''',

            )
