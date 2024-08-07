from typing import NoReturn

from src.domain.dumps.interfaces import DumpServiceInterface


class DumpServiceImplement(DumpServiceInterface):
    def __init__(
            self
    ) -> None:
        pass

    async def dump_data(self, dto: bytes) -> None:
        pass
