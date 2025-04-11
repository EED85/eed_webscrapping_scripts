FROM duckdb_tables();
FROM duckdb_views();

FROM information_layer.Pollenflug_Gefahrenindex_03_unpivot;

FROM information_layer.Pollenflug_Gefahrenindex_04_features
SELECT region_name, partregion_name,  date, pollenart, Pollenflug_Gefahrenindex_mean, *
WHERE region_id = 40 AND aktuellste_vorhersage aND Pollenflug_Gefahrenindex_mean > 0
ORDER BY date desc, pollenart desc
;

WITH _base AS (
	FROM information_layer.Pollenflug_Gefahrenindex_03_unpivot
	SELECT 
		*
		, regexp_extract(Pollenflug_Gefahrenindex , '([0-3])(-([0-3]))?', ['min', '_', 'max']) AS _Pollenflug_Gefahrenindex_min_max_regexp_
		, _Pollenflug_Gefahrenindex_min_max_regexp_['min'] AS Pollenflug_Gefahrenindex_min
		, COALESCE(IF(_Pollenflug_Gefahrenindex_min_max_regexp_['max']='', NULL, _Pollenflug_Gefahrenindex_min_max_regexp_['max']), Pollenflug_Gefahrenindex_min)  AS Pollenflug_Gefahrenindex_max
	WHERE TRUE
)
, _convert AS (
	FROM _base
	SELECT 
		* REPLACE(
			Pollenflug_Gefahrenindex_min::INT AS Pollenflug_Gefahrenindex_min
			, Pollenflug_Gefahrenindex_max::INT AS Pollenflug_Gefahrenindex_max
		)
)
, _final AS (
	FROM _convert
	SELECT 
		*
		, (Pollenflug_Gefahrenindex_max + Pollenflug_Gefahrenindex_min) / 2 AS Pollenflug_Gefahrenindex_mean
		, date_diff('DAY', last_update, date) AS vohersagetage
		, (MAX(last_update) OVER())  AS latest_update
		, CASE WHEN last_update < latest_update AND vohersagetage = 0 THEN
				TRUE
			WHEN last_update = latest_update THEN
				TRUE
			ELSE FALSE
		END AS aktuellste_vorhersage
	ORDER BY vohersagetage DESC
)
FROM _final
;


--part	date 	last_update		index
--birke	08.1.	08.1.			1		x
--birke	09.1.	08.1.			1
--birke	10.1.	08.1.			1
--birke	09.1.	09.1.			1		x
--birke	10.1.	09.1.			1
--birke	11.1.	09.1.			1
--birke	10.1.	10.1.			1		x
--birke	11.1.	10.1.			1		x
--birke	12.1.	10.1.			1		x
--
