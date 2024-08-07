from typing import NoReturn

from src.domain.dumps.interfaces import UploadDumpServiceInterface


class UploadDumpServiceImplement(UploadDumpServiceInterface):
    def __init__(
            self
    ) -> None:
        pass

    async def upload_data(self, dto: bytes) -> None:
        pass
