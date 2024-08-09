from abc import ABC, abstractmethod
from typing import NoReturn, Any


class PostgresMarketplacesRepositoryInterface(ABC):
    @abstractmethod
    async def insert_data(self, dto: dict[str, Any]) -> NoReturn:
        ...
