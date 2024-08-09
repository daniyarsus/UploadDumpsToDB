import uuid
import asyncpg

from src.infrastructure.db.postgres.interfaces import PostgresSkuRepositoryInterface
from src.infrastructure.db.postgres.dto import PostgresSKUUploadDataDTO
from src.infrastructure.db.postgres.settings import get_postgres_settings


class PostgresSkuRepositoryImplement(PostgresSkuRepositoryInterface):
    async def upload_data(
            self,
            dto: PostgresSKUUploadDataDTO
    ) -> None:
        conn = await get_postgres_settings().get_async_postgres_connect()
        async with conn.transaction():
            exists = await conn.fetchval(
                '''
                SELECT 1 FROM public.sku 
                WHERE marketplace_id = $1 AND product_id = $2 LIMIT 1;
                ''',
                dto['marketplace_id'],
                dto['product_id']
            )

            if exists:
                print(
                    f"Запись с marketplace_id={dto['marketplace_id']} и product_id={dto['product_id']} уже существует. Пропуск вставки.")
                return
            await conn.execute(
                '''
                INSERT INTO public.sku (
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
                ) 
                VALUES(
                    $1, 
                    $2, 
                    $3, 
                    $4, 
                    $5, 
                    $6, 
                    $7, 
                    $8, 
                    $9, 
                    $10, 
                    $11, 
                    $12, 
                    $13, 
                    $14, 
                    $15, 
                    $16, 
                    $17, 
                    $18, 
                    $19, 
                    $20, 
                    $21, 
                    $22, 
                    $23, 
                    $24, 
                    $25, 
                    $26, 
                    $27, 
                    $28, 
                    $29, 
                    $30, 
                    $31, 
                    $32, 
                    $33
                )
                ''',
                dto['uuid'],
                dto['marketplace_id'],
                dto['product_id'],
                dto['title'],
                dto['description'],
                dto['brand'],
                dto['seller_id'],
                dto['seller_name'],
                dto['first_image_url'],
                dto['category_id'],
                dto['category_lvl_1'],
                dto['category_lvl_2'],
                dto['category_lvl_3'],
                dto['category_remaining'],
                dto['features'],
                dto['rating_count'],
                dto['rating_value'],
                dto['price_before_discounts'],
                dto['discount'],
                dto['price_after_discounts'],
                dto['bonuses'],
                dto['sales'],
                dto['inserted_at'],
                dto['updated_at'],
                dto['currency'],
                dto['referral_url'],
                dto['barcode'],
                dto['original_url'],
                dto['mpn'],
                dto['status'],
                dto['revenue'],
                dto['images'],
                dto['last_seen_at']
            )
