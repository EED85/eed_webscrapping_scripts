from eed_webscrapping_scripts.modules import get_db_schema_from_table_name


def test_get_db_schema_from_table_name(prepare_db):
    con = prepare_db
    table_name = "db.schema.tbl"
    database_name, schema_name = get_db_schema_from_table_name(table_name, con)

    assert database_name == "db" and schema_name == "schema"
