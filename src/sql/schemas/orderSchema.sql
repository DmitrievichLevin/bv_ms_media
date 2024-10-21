CREATE TABLE orders (
    _id VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR (255) NOT NULL,
    phone VARCHAR (255) NOT NULL,
    first_name VARCHAR (255) NOT NULL,
    last_name VARCHAR (255) NOT NULL,
    address1 VARCHAR (255) NOT NULL,
    address2 VARCHAR (255),
    city VARCHAR (255) NOT NULL,
    level_1 VARCHAR (255) NOT NULL,
    zip VARCHAR (255) NOT NULL,
    total FLOAT,
    shipped TINYINT DEFAULT 0,
    tracking_no VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    country VARCHAR(2) DEFAULT 'US'
);

CREATE TABLE ordered (
    _id VARCHAR(255) UNIQUE DEFAULT NEWID(),
    order_id VARCHAR(255) NOT NULL,
    item_id VARCHAR(255) NOT NULL,
    qty INTEGER NOT NULL,
    subtotal INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (_id)
);

ALTER TABLE
    ordered
ADD
    CONSTRAINT UNIQUE_ORDERED UNIQUE CLUSTERED (_id, item_id) ON [PRIMARY]