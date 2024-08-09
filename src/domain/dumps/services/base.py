from bindme import inject
from fastapi import UploadFile

from src.domain.dumps.interfaces import UploadDumpServiceInterface
from src.domain.dumps.dto import (
    DumpsMarketplacesUploadDataDTO
)
from src.domain.dumps.usecases import (
    ProcessDataUseCase,
    InsertMarketplacesUseCase
)
from src.infrastructure.db.postgres.interfaces import PostgresMarketplacesRepositoryInterface
from src.infrastructure.db.postgres.interfaces import PostgresSkuRepositoryInterface


class UploadDumpServiceImplement(UploadDumpServiceInterface):
    @inject
    def __init__(
            self,
            postgres_marketplaces_repo: PostgresMarketplacesRepositoryInterface,
            postgres_sku_repo: PostgresSkuRepositoryInterface
    ) -> None:
        self._postgres_marketplaces_repo = postgres_marketplaces_repo
        self._postgres_sku_repo = postgres_sku_repo

    async def insert_company(
            self,
            dto: DumpsMarketplacesUploadDataDTO
    ) -> object:
        use_case = InsertMarketplacesUseCase(
            postgres_marketplaces_repo=self._postgres_marketplaces_repo
        )
        return await use_case(dto=dto)

    async def process_data(
            self,
            dto: UploadFile
    ) -> object:
        use_case = ProcessDataUseCase(
            postgres_sku_repo=self._postgres_sku_repo
        )
        return await use_case(dto=dto)
