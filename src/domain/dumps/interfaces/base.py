from abc import ABC, abstractmethod
from typing import NoReturn


class UploadDumpServiceInterface(ABC):
    @abstractmethod
    async def insert_company(self, dto: dict[str, str]) -> NoReturn:
        ...

    @abstractmethod
    async def process_data(self, dto: object) -> NoReturn:
        ...
