from fastapi import FastAPI

from .dumps import (
    UploadDumpController,
    UploadDumpServiceInterface
)


def setup_rest_controllers(app: FastAPI) -> None:
    app.include_router(
        router=UploadDumpController(
            upload_dump_service=UploadDumpServiceInterface
        ).router
    )
