import json
import uuid
import datetime

from bindme import inject

from src.domain.dumps.dto import DumpDTO
from src.domain.dumps.exceptions import (
    UploadDumpClientException,
    UploadDumpServerException
)
from src.infrastructure.db.postgres.interfaces import PostgresSkuRepositoryInterface


class ProcessDataUseCase:
    @inject
    def __init__(
            self,
            postgres_sku_repo: PostgresSkuRepositoryInterface
    ) -> None:
        self._postgres_sku_repo = postgres_sku_repo

    async def __call__(
            self,
            dto
    ) -> None:
        try:
            uuid: UUID
            marketplace_id: int
            product_id: str
            title: str
            description: Optional[str]
            brand: Optional[str]
            seller_id: Optional[str]
            seller_name: Optional[str]
            first_image_url: Optional[str]
            category_id: Optional[int]
            category_lvl_1: Optional[str]
            category_lvl_2: Optional[str]
            category_lvl_3: Optional[str]
            category_remaining: Optional[str]
            features: Optional[dict]
            rating_count: Optional[int]
            rating_value: Optional[float]
            price_before_discounts: Optional[float]
            discount: Optional[float]
            price_after_discounts: Optional[float]
            bonuses: Optional[int]
            sales: Optional[int]
            inserted_at: datetime
            updated_at: datetime
            currency: Optional[str]
            referral_url: Optional[str]
            barcode: Optional[str]
            original_url: Optional[str]
            mpn: Optional[str]
            status: Optional[str]
            revenue: Optional[float]
            images: Optional[List[str]]
            last_seen_at: datetim

            result = await self._postgres_sku_repo.upload_data(
                dto=dto
            )
            if result is None:
                raise UploadDumpClientException(
                    status_code=404,
                    message='None'
                )
        except UploadDumpClientException as client_exception:
            raise client_exception
        except BaseException as server_exception:
            raise UploadDumpServerException(
                status_code=500,
                detail=str(server_exception)
            )
