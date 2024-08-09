from datetime import datetime

from pydantic import BaseModel, Field, validator


class InsertCompanyRequest(BaseModel):
    name: str = Field(None, description="Название маркетплейса.")
    logo: str = Field(None, description="Ссылка на лого.")
    base_url: str = Field(None, description="Базовая ссылка.")
    src: str = Field(None, description="Источник информации.")
