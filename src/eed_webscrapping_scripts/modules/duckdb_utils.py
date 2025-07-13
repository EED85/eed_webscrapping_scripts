import logging
import pathlib
from pathlib import Path

import duckdb
from eed_basic_utils.os import file_exists


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


def download_database(
    source_database: str,
    target_database: str,
    con: duckdb.duckdb.DuckDBPyConnection,
    if_exists: str = "fail",
    if_error_close_connection: bool = True,
) -> bool:
    # TODO [ES-297]: add check if source_database is a motherduck database

    source_database_attached = datatbase_is_attached(source_database, con=con)
    if not source_database_attached:
        if if_error_close_connection:
            con.close()
        raise FileNotFoundError(f"File {source_database} is not attached to con.")

    target_database_exists = file_exists(f"{target_database}")
    if if_exists == "fail":
        if target_database_exists:
            if if_error_close_connection:
                con.close()
            raise FileExistsError(
                f"File {target_database} already exists. Error due to {if_exists=}"
            )
    else:
        if target_database_exists:
            target_database_attached = datatbase_is_attached(target_database, con=con)
            if target_database_attached:
                con.sql(f"DETACH {target_database}")
            pathlib.Path(target_database).unlink()
            logging.debug(f"File {target_database} deleted.")

    con.sql(f"ATTACH IF NOT EXISTS '{target_database}' AS target")
    try:
        sql = f"""COPY FROM DATABASE {source_database} TO target"""
        con.sql(sql)
        con.sql("DETACH target")
        if not file_exists(target_database):
            raise FileNotFoundError(f"File {target_database} was not created.")
        logging.info(f"Database {source_database} copied to {target_database}")
        logging.debug(f"{Path.cwd() / target_database} created.")
    except Exception as e:
        logging.error(f"Database {source_database} could not be copied to {target_database}")
        raise ValueError from e
    return True


if __name__ == "__main__":
    from eed_webscrapping_scripts.modules import connect_to_db

    cfg = {"env": {"_ENVIRONMENT_": "PROD", "_DBINSTANCE_INACTIVITY_TTL_": "1s"}}
    con = connect_to_db(cfg)
    source_db = "dwd"
    target_db = "dwd_backup.duckdb"
    # Example usage
    try:
        download_database(source_db, target_db, con, if_exists="replace")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        con.close()
    con_local = duckdb.connect(target_db)
    _d = con_local.sql("FROM duckdb_databases()").fetchall()
    print(_d)
