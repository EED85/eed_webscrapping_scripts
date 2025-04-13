USE memory;

-- Connect to Motherduck and local duckdb. Delete local duckdb please.
ATTACH IF NOT EXISTS 'C:\dev\github\EED85\eed_webscrapping_scripts\src\eed_webscrapping_scripts\dwd\local_duckdb\dwd.duckdb' AS dwd_local;
ATTACH IF NOT EXISTS 'md:dwd';

COPY FROM DATABASE dwd TO dwd_local;
DETACH dwd;
USE dwd_local;
CHECKPOINT;

-- check tables
FROM duckdb_tables() WHERE schema_name = 'datalake' ORDER BY table_name DESC;
FROM duckdb_views() WHERE schema_name IN ('information_layer');

USE memory;
DETACH dwd_local;

-- check latest view on local database
ATTACH IF NOT EXISTS 'C:\dev\github\EED85\eed_webscrapping_scripts\src\eed_webscrapping_scripts\dwd\local_duckdb\dwd.duckdb' AS dwd;
USE dwd;

FROM information_layer.Pollenflug_Gefahrenindex_03_unpivot 
WHERE TRUE
	AND region_id = 40 
	AND partregion_id = 42
ORDER BY last_update DESC, date DESC
LIMIT NULL
;
USE memory;
DETACH dwd;