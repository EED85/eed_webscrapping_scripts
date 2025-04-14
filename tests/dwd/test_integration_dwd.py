from eed_webscrapping_scripts.dwd.pollenflug_gefahrenindex import pollenflug_gefahrenindex


def test_integration_dwd():
    con = pollenflug_gefahrenindex()
    table_name = con.sql(
        "SELECT table_name FROM duckdb_tables() WHERE table_name ILIKE 'Pollenflug_Gefahrenindex%' "
    ).fetchall()[0][0]
    hash = con.sql(f"SELECT HASH(content) AS content_hash FROM datalake.{table_name}").fetchall()[
        0
    ][0]

    assert hash == 1613484728104816906
