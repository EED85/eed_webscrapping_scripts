import pytest

from eed_webscrapping_scripts.modules import get_db_schema_tbl_from_table_name


@pytest.mark.parametrize(
    "table_name, database_expected, schema_expected, table_name_expected",
    [
        ("db.schema.tbl", "db", "schema", "tbl"),
        ("schema.tbl", None, "schema", "tbl"),
        ("tbl", None, None, "tbl"),
    ],
    ids=[
        "full_path",
        "only_schema",
        "only_table",
    ],
)
def test_get_db_schema_tbl_from_table_name(
    prepare_db, table_name, database_expected, schema_expected, table_name_expected
):
    con = prepare_db
    database_expected = database_expected or con.sql("SELECT CURRENT_DATABASE()").fetchall()[0][0]
    schema_expected = schema_expected or con.sql("SELECT CURRENT_SCHEMA()").fetchall()[0][0]
    database_name, schema_name, table_name = get_db_schema_tbl_from_table_name(table_name, con)

    assert (
        database_name == database_expected
        and schema_name == schema_expected
        and table_name == table_name_expected
    )
