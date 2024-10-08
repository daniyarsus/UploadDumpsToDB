from bindme import inject
from fastapi import APIRouter, UploadFile, File, status
from fastapi.responses import JSONResponse

from src.domain.dumps.interfaces import UploadDumpServiceInterface
from src.presentation.api.rest.dumps.requests import InsertCompanyRequest


class UploadDumpController:
    @inject
    def __init__(
            self,
            upload_dump_service: UploadDumpServiceInterface
    ) -> None:
        self._upload_dump_service = upload_dump_service
        self.router = APIRouter(
            prefix="/api/v1",
            tags=["Upload Dumps API"]
        )
        self._routes()

    def _routes(self) -> None:
        @self.router.post(path="/insert-company")
        async def insert_company_endpoint(
                request: InsertCompanyRequest
        ) -> JSONResponse:
            await self._upload_dump_service.insert_company(
                dto=request
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Inserted successfully"
                }
            )

        @self.router.post(path="/process-data")
        async def process_data_endpoint(
                request: UploadFile = File(...)
        ) -> JSONResponse:
            await self._upload_dump_service.process_data(
                dto=request
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'message': 'Dump was successfully uploaded.'
                }
            )
