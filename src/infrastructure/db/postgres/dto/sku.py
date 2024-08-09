import json
from uuid import UUID
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class PostgresSKUUploadDataDTO(BaseModel):
    uuid: UUID = Field(..., description="id товара в нашей бд")
    marketplace_id: int = Field(..., description="id маркетплейса")
    product_id: Optional[str] = Field(None, description="id товара в маркетплейсе")
    title: Optional[str] = Field(None, description="название товара")
    description: Optional[str] = Field(None, description="описание товара")
    brand: Optional[str] = Field(None, description="бренд товара")
    seller_id: Optional[str] = Field(None, description="ID продавца")
    seller_name: Optional[str] = Field(None, description="Название продавца")
    first_image_url: Optional[str] = Field(None, description="URL первой картинки товара")
    category_id: Optional[int] = Field(None, description="ID категории товара")
    category_lvl_1: Optional[str] = Field(None, description="Первый уровень категории товара")
    category_lvl_2: Optional[str] = Field(None, description="Второй уровень категории товара")
    category_lvl_3: Optional[str] = Field(None, description="Третий уровень категории товара")
    category_remaining: Optional[str] = Field(None, description="Остаток категории товара")
    features: Optional[str] = Field(None, description="Характеристики товара")
    rating_count: Optional[int] = Field(None, description="Кол-во отзывов о товаре")
    rating_value: Optional[float] = Field(None, description="Рейтинг товара (0-5)")
    price_before_discounts: Optional[float] = Field(None, description="Цена до скидок")
    discount: Optional[float] = Field(None, description="Скидка")
    price_after_discounts: Optional[float] = Field(None, description="Цена после скидок")
    bonuses: Optional[int] = Field(None, description="Бонусы")
    sales: Optional[int] = Field(None, description="Продажи")
    inserted_at: datetime = Field(default_factory=datetime.now, description="Дата вставки")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата обновления")
    currency: Optional[str] = Field(None, description="Валюта")
    referral_url: Optional[str] = Field(None, description="Реферальный URL")
    barcode: Optional[str] = Field(None, description="Штрихкод")
    original_url: Optional[str] = Field(None, description="Оригинальный URL товара")
    mpn: Optional[str] = Field(None, description="MPN (Manufacturer Part Number)")
    status: Optional[str] = Field(None, description="Статус")
    revenue: Optional[float] = Field(None, description="Доход")
    images: Optional[List[str]] = Field(None, description="Список URL картинок товара")
    last_seen_at: datetime = Field(default_factory=datetime.now, description="Последний раз виден")

    @validator('features', pre=True, always=True)
    def set_features(cls, v):
        return v if v is not None else {}

    @validator('images', pre=True, always=True)
    def set_images(cls, v):
        return v if v is not None else []