from abc import ABC, abstractmethod
from typing import NoReturn


class PostgresSkuRepositoryInterface(ABC):
    @abstractmethod
    async def upload_data(self, dto: dict[str, str]) -> NoReturn:
        ...
