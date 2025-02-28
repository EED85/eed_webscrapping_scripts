WITH _tables AS (
  SELECT table_name, TRUE AS in_dwd_db FROM duckdb_tables()
  WHERE TRUE AND database_name = 'dwd'
)
, _tables_loaded AS (
  SELECT table_name, TRUE AS in_loaded_tables FROM datalake.loaded_tables
)
SELECT
  * REPLACE(COALESCE(in_dwd_db, FALSE) AS in_dwd_db, COALESCE(in_loaded_tables, FALSE) AS in_loaded_tables )
FROM _tables INNER JOIN _tables_loaded USING(table_name)
