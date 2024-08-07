from abc import ABC, abstractmethod
from typing import NoReturn


class DumpServiceInterface(ABC):
    @abstractmethod
    async def dump_data(self, dto: bytes) -> NoReturn:
        ...
