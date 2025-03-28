import duckdb


def tbl_check_if_primary_key_exists(
    table_name: str,
    primapy_key: list[str],
    con: duckdb.duckdb.DuckDBPyConnection,
    schema_name: str = None,
    database_name: str = None,
) -> bool:
    database_name = "CURRENT_DATABASE()" if database_name is None else f"'{database_name}'"
    schema_name = "CURRENT_SCHEMA()" if schema_name is None else f"'{schema_name}'"

    primary_key_exists = con.sql(f"""
            SELECT IF(COUNT(*)=0, FALSE, TRUE)
            FROM duckdb_constraints()
            WHERE TRUE
                AND database_name = {database_name}
                AND schema_name = {schema_name}
                AND table_name = '{table_name}'
                AND constraint_column_names = {str(primapy_key)}
    """).fetchall()[0][0]
    return primary_key_exists


def get_db_schema_tbl_from_table_name(
    table_name: str, con: duckdb.duckdb.DuckDBPyConnection = None
) -> list[str, str]:
    parse_table_name = table_name.split(".")
    table_name = parse_table_name[-1]
    _l_ = len(parse_table_name)
    if _l_ == 1:
        database_name = con.sql("SELECT CURRENT_DATABASE()").fetchall()[0][0]
        schema_name = con.sql("SELECT CURRENT_SCHEMA()").fetchall()[0][0]
    elif _l_ == 2:
        database_name = con.sql("SELECT CURRENT_DATABASE()").fetchall()[0][0]
        schema_name = parse_table_name[-2]
    elif _l_ == 3:
        schema_name = parse_table_name[-2]
        database_name = parse_table_name[-3]
    return database_name, schema_name, table_name


def tbl_add_primary_key(
    table_name: str,
    primapy_key: list[str],
    con: duckdb.duckdb.DuckDBPyConnection,
    if_exists: bool = True,
) -> bool:
    database_name, schema_name, table_name = get_db_schema_tbl_from_table_name(table_name)
    tbl_check_if_primary_key_exists()
    pass
