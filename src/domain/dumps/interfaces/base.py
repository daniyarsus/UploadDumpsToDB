from abc import ABC, abstractmethod
from typing import NoReturn


class UploadDumpServiceInterface(ABC):
    @abstractmethod
    async def dump_data(self, dto: bytes) -> NoReturn:
        ...
