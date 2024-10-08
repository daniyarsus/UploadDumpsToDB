DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin_user') THEN
        CREATE ROLE admin_user LOGIN;
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE base_db TO admin_user;

ALTER DATABASE base_db OWNER TO admin_user;


CREATE TABLE public.marketplaces
(
    id          integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name        text,
    logo        text,
    base_url    text,
    src         text,
    last_lookup timestamp
);

ALTER TABLE public.marketplaces
    OWNER TO admin_user;

CREATE UNIQUE INDEX marketplaces_id_uindex
    ON public.marketplaces (id);

CREATE TABLE public.sku
(
    uuid                   uuid PRIMARY KEY,
    marketplace_id         integer REFERENCES public.marketplaces(id),
    product_id             text,
    title                  text,
    description            text,
    brand                  text,
    seller_id              varchar,
    seller_name            text,
    first_image_url        text,
    category_id            integer,
    category_lvl_1         text,
    category_lvl_2         text,
    category_lvl_3         text,
    category_remaining     text,
    features               jsonb,
    rating_count           integer,
    rating_value           double precision,
    price_before_discounts real,
    discount               double precision,
    price_after_discounts  real,
    bonuses                integer,
    sales                  integer,
    inserted_at            timestamp DEFAULT now(),
    updated_at             timestamp DEFAULT now(),
    currency               text,
    referral_url           text,
    barcode                text,
    original_url           text,
    mpn                    text,
    status                 text,
    revenue                double precision,
    images                 text[],
    last_seen_at           timestamp DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON COLUMN public.sku.uuid IS 'id товара в нашей бд';
COMMENT ON COLUMN public.sku.marketplace_id IS 'id маркетплейса';
COMMENT ON COLUMN public.sku.product_id IS 'id товара в маркетплейсе';
COMMENT ON COLUMN public.sku.title IS 'название товара';
COMMENT ON COLUMN public.sku.description IS 'описание товара';
COMMENT ON COLUMN public.sku.category_lvl_1 IS 'Первая часть категории товара. Например, для товара, находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и игры/Игровые консоли, в это поле запишется "Детям".';
COMMENT ON COLUMN public.sku.category_lvl_2 IS 'Вторая часть категории товара. Например, для товара, находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и игры/Игровые консоли, в это поле запишется "Электроника".';
COMMENT ON COLUMN public.sku.category_lvl_3 IS 'Третья часть категории товара. Например, для товара, находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и игры/Игровые консоли, в это поле запишется "Детская электроника".';
COMMENT ON COLUMN public.sku.category_remaining IS 'Остаток категории товара. Например, для товара, находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и игры/Игровые консоли, в это поле запишется "Игровая консоль/Игровые консоли и игры/Игровые консоли".';
COMMENT ON COLUMN public.sku.features IS 'Характеристики товара';
COMMENT ON COLUMN public.sku.rating_count IS 'Кол-во отзывов о товаре';
COMMENT ON COLUMN public.sku.rating_value IS 'Рейтинг товара (0-5)';

ALTER TABLE public.sku
    OWNER TO admin_user;

CREATE INDEX sku_category_lvl_1_index
    ON public.sku (category_lvl_1);

CREATE INDEX sku_category_lvl_2_index
    ON public.sku (category_lvl_2);

CREATE INDEX sku_category_lvl_3_index
    ON public.sku (category_lvl_3);

CREATE UNIQUE INDEX sku_uuid_uindex
    ON public.sku (uuid);

CREATE INDEX sku_brand_index
    ON public.sku (brand);

CREATE UNIQUE INDEX sku_marketplace_id_sku_id_uindex
    ON public.sku (marketplace_id, product_id);

CREATE INDEX sku_features_index
    ON public.sku (features);

CREATE TABLE public.golden_sku
(
    uuid               uuid NOT NULL PRIMARY KEY,
    title              text,
    description        text,
    brand              text,
    first_image_url    text,
    category_id        integer,
    category_lvl_1     text,
    category_lvl_2     text,
    category_lvl_3     text,
    category_remaining text,
    features           jsonb,
    inserted_at        timestamp DEFAULT now(),
    updated_at         timestamp DEFAULT now(),
    product_id         bigint,
    uploaded_at        timestamp,
    total_revenue      double precision,
    rating             double precision,
    images             text[],
    upload_status      varchar
);

ALTER TABLE public.golden_sku
    OWNER TO admin_user;

CREATE TABLE public.golden_to_sku
(
    sku_uuid            uuid NOT NULL REFERENCES public.sku(uuid),
    match_source        text,
    matched_at          timestamp DEFAULT now(),
    verification_status boolean,
    verified_by         text,
    golden_uuid         uuid NOT NULL REFERENCES public.golden_sku(uuid),
    match_score         real,
    insales_variant_id  integer,
    verified_at         timestamp
);

COMMENT ON COLUMN public.golden_to_sku.verification_status IS 'True - подтвержденный матч. False - подтвержденный не матч. Null - unknown';

ALTER TABLE public.golden_to_sku
    OWNER TO admin_user;

CREATE UNIQUE INDEX golden_to_sku_sku_uuid_golden_uuid_match_source_uindex
    ON public.golden_to_sku (sku_uuid, golden_uuid, match_source);

CREATE INDEX golden_sku_features_index
    ON public.golden_sku (features);

CREATE TABLE public.categories
(
    marketplace_category  text NOT NULL PRIMARY KEY,
    gs_category_lvl_1     text,
    gs_category_lvl_2     text,
    gs_category_lvl_3     text,
    marketplace_id        integer,
    active                boolean DEFAULT false,
    insales_category_id   integer,
    insales_image         text,
    insales_collection_id integer,
    description           text,
    html_title            text,
    seo_description       text,
    meta_description      text,
    meta_keywords         text
);

ALTER TABLE public.categories
    OWNER TO admin_user;

CREATE TABLE public.price_history
(
    sku_uuid              uuid REFERENCES public.sku(uuid),
    price_after_discount  double precision,
    price_before_discount real,
    discount              double precision,
    sales                 integer,
    revenue               double precision,
    updated_at            timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.price_history
    OWNER TO admin_user;

CREATE TABLE public.goodsale_offers
(
    uuid                   uuid NOT NULL PRIMARY KEY,
    status                 varchar(255),
    price_before_discounts double precision,
    price_after_discounts  double precision,
    golden_uuid            uuid NOT NULL REFERENCES public.golden_sku(uuid),
    insales_variant_id     integer
);

ALTER TABLE public.goodsale_offers
    OWNER TO admin_user;

CREATE FUNCTION public.update_price_history() RETURNS trigger
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO price_history (
        sku_uuid,
        price_after_discount,
        price_before_discount,
        discount,
        sales,
        revenue,
        updated_at
    )
    VALUES (
        OLD.uuid,
        OLD.price_after_discounts,
        OLD.price_before_discounts,
        OLD.discount,
        OLD.sales,
        OLD.revenue,
        CURRENT_TIMESTAMP
    );
    RETURN NULL;
END;
$$;

ALTER FUNCTION public.update_price_history() OWNER TO admin_user;

CREATE TRIGGER trg_update_price_history
    BEFORE UPDATE
        OF price_after_discounts, price_before_discounts
    ON public.sku
    FOR EACH ROW
    WHEN (OLD.price_after_discounts IS DISTINCT FROM NEW.price_after_discounts OR
          OLD.price_before_discounts IS DISTINCT FROM NEW.price_before_discounts)
    EXECUTE PROCEDURE public.update_price_history();
