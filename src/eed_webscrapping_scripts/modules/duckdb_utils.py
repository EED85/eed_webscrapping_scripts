import duckdb


def check_if_primary_key_exists(
    table_name: str,
    con: duckdb.duckdb.DuckDBPyConnection,
    schema_name: str = None,
    database_name: str = None,
) -> bool:
    database_name = "CURRENT_DATABASE()" if database_name is None else f"'{database_name}'"
    schema_name = "CURRENT_SCHEMA()" if schema_name is None else f"'{schema_name}'"
    sql = f"""
            SELECT IF(COUNT(*) = 0, FALSE, TRUE)
            FROM duckdb_constraints()
            WHERE TRUE
                AND database_name = {database_name}
                AND schema_name = {schema_name}
                AND table_name = '{table_name}'
                AND constraint_type = 'PRIMARY KEY'
    """
    primary_key_exists = con.sql(sql).fetchall()[0][0]
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


def add_primary_key(
    table_name: str,
    primary_key: tuple[str] | set[str] | list[str],
    con: duckdb.duckdb.DuckDBPyConnection,
    if_exists: str = "fail",
) -> bool:
    database_name, schema_name, table_name = get_db_schema_tbl_from_table_name(table_name, con=con)
    primary_key_exists = check_if_primary_key_exists(
        table_name=table_name,
        con=con,
        schema_name=schema_name,
        database_name=database_name,
    )
    primary_key_was_added = False
    if primary_key_exists and if_exists == "fail":
        raise ValueError(f"""
            {primary_key=} already exists on Table {table_name=}
        """)
    elif primary_key_exists and if_exists != "fail":
        pass
    elif not primary_key_exists:
        pk = str(tuple(primary_key)).replace("'", "")
        sql = f"""
            ALTER TABLE {database_name}.{schema_name}.{table_name}
            ADD PRIMARY KEY {pk}
        """
        con.sql(sql)
        primary_key_was_added = True
    else:
        raise ValueError(f""" not implemented for {primary_key_exists=}, {if_exists=} """)
    return primary_key_was_added


def datatbase_is_attached(database_name: str, con: duckdb.duckdb.DuckDBPyConnection = None) -> bool:
    """
    Checks if a database is attached to the current DuckDB connection.

    Parameters
    ----------
    database_name : str
        The name of the database to check.
    con : duckdb.duckdb.DuckDBPyConnection, optional
        The DuckDB connection to use. If no connection is provided, a new connection will be created.

    Returns
    -------
    bool
        True if the database is attached, False otherwise.
    """
    con = con or duckdb.connect()
    sql = f"""
        SELECT COUNT(*) > 0 AS database_is_attached
        FROM duckdb_databases()
        WHERE database_name = '{database_name}'
    """
    datatbase_is_attached = con.sql(sql).fetchall()[0][0]
    return datatbase_is_attached


# def copy_database(
#     source_database: str,
#     target_database: str,
#     con: duckdb.duckdb.DuckDBPyConnection = None,
#     if_exists: str = "fail",
# ) -> bool:
#     con = con or duckdb.connect()

#     target_database_exists = file_exists(f"{target_database}.duckdb")
#     source_database_exists = file_exists(f"{source_database}.duckdb")

#     if not target_database_exists and if_exists == "fail":
#         raise FileExistsError(f"File {target_database} already exists.")
#     if not source_database_exists:
#         raise FileNotFoundError(f"File {source_database} does not exist.")

#     con.sql(f"ATTACH IF NOT EXISTS '{source_database}' AS source")
#     con.sql(f"ATTACH IF NOT EXISTS '{target_database}' AS target")
#     sql = f"""
#         COPY source TO target
#     """
#     con.sql(sql)
#     return True
