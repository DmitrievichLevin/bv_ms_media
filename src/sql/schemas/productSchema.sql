CREATE TABLE product (
    -- uuid
    id VARCHAR(255) NOT NULL UNIQUE,
    -- name
    item_name VARCHAR(255) NOT NULL,
    -- variation
    item_variation VARCHAR(255),
    -- price
    item_price VARCHAR(255) NOT NULL,
    -- item description
    item_desc VARCHAR(255) NOT NULL,
    -- # Orders placed
    orders INTEGER DEFAULT 0,
    --
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- Index Mongo Doc For Optimized Query on Document Media
    INDEX fk_produc_name (item_name ASC)
);

-- Media exists once per document-property
ALTER TABLE
    [dbo].[product]
ADD
    CONSTRAINT UNIQUE_PRODUCT UNIQUE CLUSTERED (
        id,
        item_name,
        item_variation
    ) ON [PRIMARY]