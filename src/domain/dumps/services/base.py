from bindme import inject

from src.domain.dumps.interfaces import UploadDumpServiceInterface
from src.domain.dumps.dto import DumpDTO
from src.domain.dumps.usecases import ProcessDataUseCase
from src.infrastructure.db.postgres.interfaces import PostgresSkuRepositoryInterface


class UploadDumpServiceImplement(UploadDumpServiceInterface):
    @inject
    def __init__(
            self,
            postgres_sku_repo: PostgresSkuRepositoryInterface
    ) -> None:
        self._postgres_sku_repo = postgres_sku_repo

    async def process_data(self, dto) -> None:
        use_case = ProcessDataUseCase(
            postgres_sku_repo=self._postgres_sku_repo
        )
        await use_case(dto=dto)
