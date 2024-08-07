import asyncio
import asyncpg
import json
import uuid
from datetime import datetime

# Пример JSON данных
sample_json = {
    "id": "344423",
    "name": "Шкаф коммутационный ЦМО ШРН-М-12.650.1 настенный,  металлическая передняя дверь,  12U,  600x650 мм",
    "images": [
        "https://cdn.citilink.ru/VIyEcriqskiM5pRBYIZnQiRPxqwr9RAfu9bzE8KB0kw/gravity:sm/height:900/resizing_type:fit/width:900/plain/items/344423_v01_b.jpg",
        "https://cdn.citilink.ru/fLtY80Y5B4BEcslMkb-QK4vdBTKTsQeSBxXjQIdIKX0/gravity:sm/height:900/resizing_type:fit/width:900/plain/items/344423_v02_b.jpg",
        "https://cdn.citilink.ru/AQZWosgVFJo6igjwVRytZtBGNJrCfTeWN_-Rh4nA8Eg/gravity:sm/height:900/resizing_type:fit/width:900/plain/items/344423_v03_b.jpg",
        "https://cdn.citilink.ru/MyXIDyBpje61g4QUZy1k0T2O1EDXRZJ6YBhQ57o76qA/gravity:sm/height:900/resizing_type:fit/width:900/plain/items/344423_v04_b.jpg",
        "https://cdn.citilink.ru/v58sE_Xlh3MOSTdoTIjpXvaK6cBidbcNNvlWFSab_cs/gravity:sm/height:900/resizing_type:fit/width:900/plain/items/344423_v05_b.jpg",
        "https://cdn.citilink.ru/g4SnJEVkOosOYcSC0cOTyiREnMTPezDwo-V5F25uVtk/gravity:sm/height:900/resizing_type:fit/width:900/plain/items/344423_v06_b.jpg",
        "https://cdn.citilink.ru/vSa3a8tl65VvR48hoebGIGeRL5weQQjXzzNkudFhj4A/gravity:sm/height:900/resizing_type:fit/width:900/plain/items/344423_v07_b.jpg"
    ],
    "brand": "ЦМО",
    "category": {
        "id": "1010"
    },
    "variations": [
        {
            "id": "344423",
            "price": 19230,
            "msrp": 19230,
            "inventory": 1,
            "image": "https://cdn.citilink.ru/VIyEcriqskiM5pRBYIZnQiRPxqwr9RAfu9bzE8KB0kw/gravity:sm/height:900/resizing_type:fit/width:900/plain/items/344423_v01_b.jpg",
            "promo": 17970,
            "isAvailable": True
        }
    ]
}

async def insert_data(json_data):
    # Подключение к базе данных
    conn = await asyncpg.connect(
        user='admin_user',
        password='your_password',  # Обновите с вашим паролем
        database='main',
        host='localhost'
    )

    try:
        # Извлечение необходимых данных
        product_id = json_data["id"]
        title = json_data["name"]
        images = json_data["images"]
        brand = json_data["brand"]
        category_id = int(json_data["category"]["id"])

        # Предполагаем, что первая вариация содержит необходимые детали о ценах
        variation = json_data["variations"][0]
        price_after_discounts = float(variation["price"])
        price_before_discounts = float(variation["msrp"])
        discount = price_before_discounts - price_after_discounts
        sales = int(variation["inventory"])
        first_image_url = variation["image"]
        is_available = variation["isAvailable"]

        # Генерация UUID для нового SKU
        sku_uuid = uuid.uuid4()

        # Установка некоторых полей по умолчанию
        marketplace_id = 1  # Предполагаем, что '1' это временное значение; обновите по необходимости
        currency = 'RUB'  # Предполагаем, что валюта рубли
        status = 'available' if is_available else 'unavailable'
        inserted_at = datetime.now()
        updated_at = datetime.now()
        description = ""
        seller_id = ""
        seller_name = ""
        category_lvl_1 = ""
        category_lvl_2 = ""
        category_lvl_3 = ""
        category_remaining = ""
        features = json.dumps({})
        rating_count = 0
        rating_value = 0.0
        bonuses = 0
        referral_url = ""
        barcode = ""
        original_url = ""
        mpn = ""
        revenue = 0.0

        # Вставка данных в таблицу `sku` используя параметризованные запросы
        await conn.execute('''
            INSERT INTO public.sku(
                uuid, marketplace_id, product_id, title, description, brand, 
                seller_id, seller_name, first_image_url, category_id, 
                category_lvl_1, category_lvl_2, category_lvl_3, category_remaining, 
                features, rating_count, rating_value, price_before_discounts, 
                discount, price_after_discounts, bonuses, sales, inserted_at, 
                updated_at, currency, referral_url, barcode, original_url, mpn, 
                status, revenue, images, last_seen_at
            ) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, 
                      $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, 
                      $29, $30, $31, $32, $33, $34)
        ''', sku_uuid, marketplace_id, product_id, title, description, brand,
           seller_id, seller_name, first_image_url, category_id,
           category_lvl_1, category_lvl_2, category_lvl_3, category_remaining,
           features, rating_count, rating_value, price_before_discounts,
           discount, price_after_discounts, bonuses, sales, inserted_at,
           updated_at, currency, referral_url, barcode, original_url, mpn,
           status, revenue, images, datetime.now())

        print(f"Inserted SKU with UUID: {sku_uuid}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Закрытие соединения
        await conn.close()

# Запуск функции вставки данных
asyncio.run(insert_data(sample_json))
