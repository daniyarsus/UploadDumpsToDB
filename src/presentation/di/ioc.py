from bindme import container

from src.domain.dumps.interfaces import UploadDumpServiceInterface
from src.domain.dumps.services import UploadDumpServiceImplement
from src.infrastructure.db.postgres.interfaces import PostgresSkuRepositoryInterface
from src.infrastructure.db.postgres.repositories import PostgresSkuRepositoryImplement


def setup_ioc(container: container) -> None:
    container.register(
        abstract_class=UploadDumpServiceInterface,
        concrete_class=UploadDumpServiceImplement
    )
    container.register(
        abstract_class=PostgresSkuRepositoryInterface,
        concrete_class=PostgresSkuRepositoryImplement
    )
