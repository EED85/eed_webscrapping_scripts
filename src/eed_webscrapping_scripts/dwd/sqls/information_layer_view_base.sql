WITH _base AS (
SELECT
	*,
	unnest(content) AS content_unnest,
FROM datalake.Pollenflug_Gefahrenindex
)
, _u2 AS (
	SELECT
		content_unnest.region_name
		, content_unnest.region_id
		, content_unnest.partregion_name
		, content_unnest.partregion_id
		, last_update
		, next_update
		, unnest(content_unnest.Pollen) AS _pollen
	FROM _base
)
SELECT
    * REPLACE(
        strptime(last_update, '%Y-%m-%d %H:%M Uhr') AS last_update
        , strptime(next_update, '%Y-%m-%d %H:%M Uhr') AS next_update
    )
FROM _u2
