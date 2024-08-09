from abc import ABC, abstractmethod
from typing import NoReturn, Any


class PostgresSkuRepositoryInterface(ABC):
    @abstractmethod
    async def upload_data(self, dto: dict[str, Any]) -> NoReturn:
        ...
