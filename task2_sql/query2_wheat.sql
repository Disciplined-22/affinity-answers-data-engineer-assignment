-- task2_sql/query2_longest_wheat_dna.sql

SELECT 
    t.species,
    r.rfamseq_acc,
    r.length AS dna_sequence_length
FROM taxonomy t
JOIN rfamseq r ON t.ncbi_id = r.ncbi_id
WHERE t.tax_string LIKE '%Triticum%' OR t.species LIKE '%wheat%'
ORDER BY r.length DESC
LIMIT 1;


-- Note on Table Join:
-- Performed an INNER JOIN between `taxonomy` and `rfamseq` using primary key `ncbi_id`.

-- Note on Query Logic:
-- We search `tax_string LIKE '%Triticum%'` because Triticum is the botanical genus for wheat.
-- Most wheat records use scientific names (e.g., 'Triticum aestivum') rather than the word 'wheat'.
-- Filtering by 'Triticum' in `tax_string` ensures all genuine wheat species are accurately captured across the taxonomy tree.

-- Note on Performance:
-- Query execution time may vary depending on the public Rfam database load and server latency.