import json
import uuid
import datetime
from typing import List
from fastapi import UploadFile
from bindme import inject

from src.domain.dumps.dto import DumpsMarketplacesUploadDataDTO
from src.domain.dumps.exceptions import UploadDumpClientException, UploadDumpServerException
from src.infrastructure.db.postgres.interfaces import PostgresMarketplacesRepositoryInterface, PostgresSkuRepositoryInterface

class ProcessDataUseCase:
    @inject
    def __init__(
            self,
            postgres_sku_repo: PostgresSkuRepositoryInterface
    ) -> None:
        self._postgres_sku_repo = postgres_sku_repo

    async def __call__(
            self,
            dto: UploadFile
    ) -> None:
        try:
            content = await dto.read()
            json_lines = content.decode('utf-8').splitlines()
            json_data_list = [json.loads(line) for line in json_lines]

            print(f"Прочитано {len(json_data_list)} JSON записей из файла.")
            await self.process_json_stream(json_data_list)
        except UploadDumpClientException as client_exception:
            print(f"Ошибка клиента: {client_exception}")
            raise client_exception
        except BaseException as server_exception:
            print(f"Ошибка сервера: {server_exception}")
            raise server_exception

    async def insert_data(self, json_data: dict) -> None:
        try:
            product_id = json_data.get("id")
            title = json_data.get("name")
            images = json_data.get("images", [])
            brand = json_data.get("brand")
            category_id = int(json_data["category"]["id"]) if "category" in json_data else None

            variation = json_data["variations"][0] if "variations" in json_data and json_data["variations"] else {}
            price_after_discounts = float(variation.get("price", 0))
            price_before_discounts = float(variation.get("msrp", 0))
            discount = price_before_discounts - price_after_discounts if price_before_discounts and price_after_discounts else None
            sales = int(variation.get("inventory", 0))
            first_image_url = variation.get("image")
            is_available = variation.get("isAvailable", True)

            sku_uuid = uuid.uuid4()

            marketplace_id = 1
            currency = 'RUB'
            status = 'available' if is_available else 'unavailable'
            inserted_at = datetime.datetime.now()
            updated_at = datetime.datetime.now()
            description = json_data.get("description", "")
            seller_id = json_data.get("seller_id", "")
            seller_name = json_data.get("seller_name", "")

            category_path = json_data.get("category", {}).get("path", [])
            category_lvl_1 = category_path[0] if len(category_path) > 0 else ""
            category_lvl_2 = category_path[1] if len(category_path) > 1 else ""
            category_lvl_3 = category_path[2] if len(category_path) > 2 else ""
            category_remaining = " > ".join(category_path[3:])

            features = json.dumps(json_data.get("features", {}))
            rating_count = json_data.get("rating_count", 0)
            rating_value = json_data.get("rating_value", 0.0)
            bonuses = json_data.get("bonuses", 0)
            referral_url = json_data.get("referral_url", "")
            barcode = json_data.get("barcode", "")
            original_url = json_data.get("original_url", "")
            mpn = json_data.get("mpn", "")
            revenue = json_data.get("revenue", 0.0)

            data = {
                "uuid": str(sku_uuid),
                "marketplace_id": marketplace_id,
                "product_id": product_id,
                "title": title,
                "description": description,
                "brand": brand,
                "seller_id": seller_id,
                "seller_name": seller_name,
                "first_image_url": first_image_url,
                "category_id": category_id,
                "category_lvl_1": category_lvl_1,
                "category_lvl_2": category_lvl_2,
                "category_lvl_3": category_lvl_3,
                "category_remaining": category_remaining,
                "features": features,
                "rating_count": rating_count,
                "rating_value": rating_value,
                "price_before_discounts": price_before_discounts,
                "discount": discount,
                "price_after_discounts": price_after_discounts,
                "bonuses": bonuses,
                "sales": sales,
                "inserted_at": inserted_at,
                "updated_at": updated_at,
                "currency": currency,
                "referral_url": referral_url,
                "barcode": barcode,
                "original_url": original_url,
                "mpn": mpn,
                "status": status,
                "revenue": revenue,
                "images": images,
                "last_seen_at": datetime.datetime.now()
            }

            await self._postgres_sku_repo.upload_data(dto=data)

            print(f"Вставлен SKU с UUID: {sku_uuid} и Product ID: {product_id}")

        except BaseException as server_exception:
            print(f"Ошибка при обработке Product ID: {json_data.get('id')}. Ошибка: {server_exception}")
            raise server_exception

    async def process_json_stream(
            self,
            json_stream: List[dict],
            batch_size: int = 100
    ) -> None:
        total_records = len(json_stream)
        print(f"Обработка {total_records} записей пакетами по {batch_size}.")

        for i in range(0, total_records, batch_size):
            batch = json_stream[i:i + batch_size]
            print(f"Обработка пакета {i // batch_size + 1}/{(total_records // batch_size) + 1}. Размер пакета: {len(batch)}")
            for item in batch:
                await self.insert_data(item)

        print("Завершена обработки всех записей.")

class InsertMarketplacesUseCase:
    @inject
    def __init__(
            self,
            postgres_marketplaces_repo: PostgresMarketplacesRepositoryInterface
    ) -> None:
        self._postgres_marketplaces_repo = postgres_marketplaces_repo

    async def __call__(
            self,
            dto: DumpsMarketplacesUploadDataDTO
    ) -> None:
        try:
            await self._postgres_marketplaces_repo.insert_data(dto=dto)
        except BaseException as server_exception:
            raise server_exception
