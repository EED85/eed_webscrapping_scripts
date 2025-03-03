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
