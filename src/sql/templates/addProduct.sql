-- EXEC dbo.createProduct 'MIWYHLJ3YDEO7HYC2GPDLTGR','Cashews'
-- ,'These aren''t just a delicious treat; they''re an
-- ode to America''s favorite nut. Whether you
--         wish to collect memorabilia to commemorate
--         45, or express that you''ve
--         exhausted just about every mental faculty trying to figure out what
--         "non-binary" means. One things for certain, another four years of
--         Sleepy Joe & Co. and we won''t be able to identify as
--         America. This
--         limited edition offering is the
--         best gift for your liberal
--         constituents.',40,'Unsalted';
-- SELECT
--     p.id,
--     p.item_name,
--     p.item_variation,
--     SUM(p.item_price * 5) as TOTAL
-- FROM
--     product as p
-- WHERE
--     p.id = 'MIWYHLJ3YDEO7HYC2GPDLTGR'
-- GROUP BY
--     id,
--     item_name,
--     item_variation;
SELECT
    *
FROM
    orders;