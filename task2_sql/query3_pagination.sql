-- task2_sql/query3_family_pagination.sql

SELECT 
    f.rfam_acc,
    f.rfam_id AS family_name,
    MAX(r.length) AS max_sequence_length
FROM rfamseq r
JOIN full_region fr ON r.rfamseq_acc = fr.rfamseq_acc
JOIN family f ON fr.rfam_acc = f.rfam_acc
WHERE r.length > 1000000
  AND fr.is_significant = 1
GROUP BY f.rfam_acc, f.rfam_id
ORDER BY max_sequence_length DESC
LIMIT 15 OFFSET 120;


/* -----------------------------------------------------------------------------
 * 1. Pagination Calculation
 * -----------------------------------------------------------------------------
 *
 * To fetch Page 9 with a Page Size of 15 results:
 *
 * OFFSET = (Page Number - 1) × Page Size
 *        = (9 - 1) × 15
 *        = 120
 *
 * Resulting Clause: LIMIT 15 OFFSET 120
 * ----------------------------------------------------------------------------- */

/* -----------------------------------------------------------------------------
 * 2. Table Connection & Data Flow
 * -----------------------------------------------------------------------------
 * To retrieve the family details along with the max DNA sequence length, 
 * three tables must be joined:
 *
 * 1. family (f): Contains family metadata (rfam_acc, rfam_id).
 * 2. full_region (fr): Junction table linking RNA families to specific genomic 
 *    sequence regions (rfam_acc <-> rfamseq_acc).
 * 3. rfamseq (r): Contains sequence metadata, including total sequence length (length).
 *
 * Table Relationship Diagram:
 *
 * [ family (f) ]                [ full_region (fr) ]               [ rfamseq (r) ]
 * rfam_acc | rfam_id            rfam_acc | rfamseq_acc             rfamseq_acc | length
 * ------------------            ----------------------             --------------------
 * RF00001  | 5S_rRNA  <-------> RF00001  | CM000350.1  <---------> CM000350.1  | 1,200,000
 * RF00002  | tRNA     <-------> RF00002  | LT934116.1  <---------> LT934116.1  | 800,000
 */


/* -----------------------------------------------------------------------------
 * 3. Performance Analysis & Execution Bottlenecks
 * -----------------------------------------------------------------------------
 * Execution Time: ~12 to 15+ minutes in DBeaver / GUI clients.
 *
 * Key Reasons for High Execution Time:
 *
 * A. Unindexed `length` Column (Full Table Scan):
 *    - The `length` column in `rfamseq` is an unindexed attribute.
 *    - Evaluating `WHERE r.length > 1000000` requires MySQL to scan tens of 
 *      millions of rows in `rfamseq` rather than utilizing a fast index lookup.
 *
 * B. Massive Join Volume on `full_region`:
 *    - The `full_region` table contains over 100 million records.
 *    - Joining millions of candidate sequences across `full_region` forces 
 *      heavy disk I/O and temporary table creation for the `GROUP BY` operation.
 *
 * C. Remote Public Server & Network Latency:
 *    - The public server (mysql-rfam-public.ebi.ac.uk) enforces strict resource 
 *      limits and experiences high concurrent usage, compounding I/O latency 
 *      over public connections.
 */