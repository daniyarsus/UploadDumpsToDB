import asyncio
import asyncpg
import json
import uuid
from datetime import datetime

# Sample JSON data
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
    # Connect to the database
    conn = await asyncpg.connect(
        user='admin_user',
        password='your_password',  # Update with actual password
        database='main',
        host='localhost'
    )

    try:
        # Extract necessary data
        product_id = json_data["id"]
        title = json_data["name"]
        images = json_data["images"]
        brand = json_data["brand"]
        category_id = int(json_data["category"]["id"])

        # Assume the first variation contains the relevant pricing details
        variation = json_data["variations"][0]
        price_after_discounts = float(variation["price"])
        price_before_discounts = float(variation["msrp"])
        discount = price_before_discounts - price_after_discounts
        inventory = int(variation["inventory"])
        first_image_url = variation["image"]
        is_available = variation["isAvailable"]

        # Generate a UUID for the new SKU
        sku_uuid = uuid.uuid4()

        # Set some of the default fields
        marketplace_id = 1  # Assuming '1' is a placeholder; adjust based on actual marketplace data
        currency = 'RUB'  # Assuming Russian rubles
        status = 'available' if is_available else 'unavailable'
        inserted_at = datetime.now()
        updated_at = datetime.now()

        # Insert data into the `sku` table
        await conn.execute('''
            INSERT INTO public.sku(
                uuid, marketplace_id, product_id, title, brand, first_image_url,
                category_id, price_before_discounts, price_after_discounts, 
                discount, sales, inserted_at, updated_at, currency, images, status
            ) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
        ''',
        sku_uuid, marketplace_id, product_id, title, brand, first_image_url,
        category_id, price_before_discounts, price_after_discounts, discount,
        inventory, inserted_at, updated_at, currency, images, status
        )

        print(f"Inserted SKU with UUID: {sku_uuid}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        await conn.close()


# Run the insert function
asyncio.run(insert_data(sample_json))
