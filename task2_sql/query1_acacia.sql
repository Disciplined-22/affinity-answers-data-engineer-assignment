-- task2_sql/query1_acacia_count.sql

-- Query (using species as Direct Source of Truth):
-- Querying purely against `species` yields the count (389).
--
SELECT COUNT(*) AS acacia_species_count
FROM taxonomy
WHERE species LIKE '%Acacia%';