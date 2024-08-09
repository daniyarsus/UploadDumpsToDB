from fastapi.exceptions import HTTPException


class UploadDumpClientException(HTTPException):
    def __init__(
            self,
            status_code: int,
            detail: str
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail
        )


class UploadDumpServerException(HTTPException):

    def __init__(
            self,
            status_code: int,
            detail: str
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail
        )
