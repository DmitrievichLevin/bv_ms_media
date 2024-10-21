-- =======================================================
-- Create Product Procedure
-- =======================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:      Dmitrievich Levin
-- Create Date: 08/2/2024
-- Description: Create Product Row.
-- =============================================
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE type = 'P' AND OBJECT_ID = OBJECT_ID('createProduct'))
   exec('CREATE PROCEDURE [dbo].[createProduct] AS BEGIN SET NOCOUNT ON; END')
GO
ALTER PROCEDURE [dbo].[createProduct]
    (
    @product_id VARCHAR(255),
    @product_name VARCHAR(255),
    @product_desc VARCHAR(255),
    @price INTEGER,
    @product_variation VARCHAR(255)
)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON

    DECLARE @newProduct TABLE (id VARCHAR(255),
        item_name VARCHAR(255),
        item_desc VARCHAR(255),
        item_price INTEGER,
        item_variation VARCHAR(255),
        orders INTEGER DEFAULT 0,
        created_at DATETIME
            DEFAULT CURRENT_TIMESTAMP
         )

    -- Create Product WHERE NOT EXISTS
    INSERT INTO product
        (id, item_name, item_desc, item_price, item_variation)
    VALUES
        (@product_id, @product_name, @product_desc, @price, @product_variation)


    SELECT *
    FROM @newProduct
END
GO
