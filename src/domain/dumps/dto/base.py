from pydantic import BaseModel


class DumpDTO(BaseModel):
    content: bytes
