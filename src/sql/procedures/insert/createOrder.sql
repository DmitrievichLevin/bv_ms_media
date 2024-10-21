-- =======================================================
-- Media Meta-Data
-- =======================================================
SET
    ANSI_NULLS ON
GO
SET
    QUOTED_IDENTIFIER ON
GO
    -- =============================================
    -- Author:      Dmitrievich Levin
    -- Create Date: 07/16/2024
    -- Description: Creates Media metadata and guest(if not exists).
    -- =============================================
    IF NOT EXISTS (
        SELECT
            *
        FROM
            sys.objects
        WHERE
            type = 'P'
            AND OBJECT_ID = OBJECT_ID('createOrder')
    ) exec(
        'CREATE PROCEDURE [dbo].[createOrder] AS BEGIN SET NOCOUNT ON; END'
    )
GO
    ALTER PROCEDURE [dbo].[createOrder] (
        -- params
        @email VARCHAR (255),
        @phone VARCHAR (255),
        @items VARCHAR (255),
        @qtys VARCHAR (255),
        @first_name VARCHAR (255),
        @last_name VARCHAR (255),
        @address1 VARCHAR (255),
        @address2 VARCHAR (255),
        @city VARCHAR (255),
        @level_1 VARCHAR (255),
        @zip VARCHAR (255)
    ) AS BEGIN;

DECLARE @id TABLE (_id VARCHAR(255));

-- CREATES ORDER ROW
INSERT INTO
    dbo.orders (
        _id,
        email,
        phone,
        first_name,
        last_name,
        address1,
        address2,
        city,
        level_1,
        zip
    ) OUTPUT INSERTED._id INTO @id
VALUES
    (
        NEWID(),
        @email,
        @phone,
        @first_name,
        @last_name,
        @address1,
        @address2,
        @city,
        @level_1,
        @zip
    );

DECLARE @subtotals TABLE (subtotal INTEGER);

-- CREATES ORDERED ROWS WITH ORDER_ID
INSERT INTO
    dbo.ordered (item_id, qty, subtotal, order_id) OUTPUT INSERTED.subtotal INTO @subtotals
SELECT
    *
FROM
    (
        SELECT
            item_id,
            qty,
            SUM(product.item_price * CAST(qty AS INTEGER)) AS subtotal
        FROM
            (
                SELECT
                    item.value AS item_id,
                    qty.value AS qty
                FROM
                    (
                        SELECT
                            *
                        FROM
                            STRING_SPLIT(@items, ',', 1)
                    ) item
                    JOIN (
                        SELECT
                            *
                        FROM
                            STRING_SPLIT(@qtys, ',', 1)
                    ) qty ON item.ordinal = qty.ordinal
            ) AS ordered,
            dbo.product AS product
        WHERE
            product.id = ordered.item_id
        GROUP BY
            item_id,
            qty
    ) line_item,
    (
        SELECT
            _id AS order_id
        FROM
            @id
    ) o;

-- Update order row with total
UPDATE
    O
SET
    total = (
        SELECT
            SUM(subtotal) AS total
        FROM
            @subtotals
    )
FROM
    dbo.orders O,
    @id I
WHERE
    O._id = I._id;

-- Add shipping to total if total < 100
UPDATE
    O
SET
    total = total + 14.99
FROM
    dbo.orders O,
    @id I
WHERE
    O._id = I._id
    AND O.total < 100;

SELECT
    *,
    DATEDIFF(SECOND, '1970-01-01', O.created_at) AS created_at
FROM
    dbo.orders O,
    @id I
WHERE
    O._id = I._id;

RETURN;

END
GO