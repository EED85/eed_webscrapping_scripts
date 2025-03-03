(
	FROM dwd.information_layer.Pollenflug_Gefahrenindex_01_base
	SELECT region_name,
		region_id,
		partregion_name,
		partregion_id,
		last_update,
		next_update,
		last_update::DATE AS date,
		Roggen.today::STRING AS Roggen,
		Birke.today::STRING AS Birke,
		Hasel.today::STRING AS Hasel,
		Ambrosia.today::STRING AS Ambrosia,
		Beifuss.today::STRING AS Beifuss,
		Graeser.today::STRING AS Graeser,
		Erle.today::STRING AS Erle,
		Esche.today::STRING AS Esche
)
UNION
BY NAME (
	FROM dwd.information_layer.Pollenflug_Gefahrenindex_01_base
	SELECT region_name,
		region_id,
		partregion_name,
		partregion_id,
		last_update,
		next_update,
		last_update::DATE + INTERVAL 1 DAY AS date,
		Roggen.tomorrow::STRING AS Roggen,
		Birke.tomorrow::STRING AS Birke,
		Hasel.tomorrow::STRING AS Hasel,
		Ambrosia.tomorrow::STRING AS Ambrosia,
		Beifuss.tomorrow::STRING AS Beifuss,
		Graeser.tomorrow::STRING AS Graeser,
		Erle.tomorrow::STRING AS Erle,
		Esche.tomorrow::STRING AS Esche
)
UNION
BY NAME (
	FROM dwd.information_layer.Pollenflug_Gefahrenindex_01_base
	SELECT region_name,
		region_id,
		partregion_name,
		partregion_id,
		last_update,
		next_update,
		last_update::DATE + INTERVAL 2 DAY AS date,
		Roggen.dayafter_to::STRING AS Roggen,
		Birke.dayafter_to::STRING AS Birke,
		Hasel.dayafter_to::STRING AS Hasel,
		Ambrosia.dayafter_to::STRING AS Ambrosia,
		Beifuss.dayafter_to::STRING AS Beifuss,
		Graeser.dayafter_to::STRING AS Graeser,
		Erle.dayafter_to::STRING AS Erle,
		Esche.dayafter_to::STRING AS Esche
)
