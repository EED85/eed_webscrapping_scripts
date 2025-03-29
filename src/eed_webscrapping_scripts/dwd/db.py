from eed_webscrapping_scripts.modules import connect_to_db


def prepare_db(cfg, con=None):
    """Prepares dwd database.

    Args:
        con (Duckdb / Motherduck connection, optional):
            Defaults to None. if ommited, con is created via ``connect_to_db()``.

    Returns:
        Duckdb / Motherduck connection:
        Useful, if con has been ommitted by inputargs.
    """

    con = con or connect_to_db(cfg)
    if cfg["runs_on_ga"]:
        con.sql("CREATE DATABASE IF NOT EXISTS dwd")
    con.sql("USE dwd")
    con.sql("CREATE SCHEMA IF NOT EXISTS datalake")
    con.sql("CREATE SCHEMA IF NOT EXISTS information_layer")
    con.sql(
        """
        CREATE TABLE IF NOT EXISTS datalake.loaded_tables(
            table_name VARCHAR PRIMARY KEY
            , last_update timestamp
            , inserttimestamptz TIMESTAMPTZ DEFAULT GET_CURRENT_TIMESTAMP()
        );
    """
    )
    return con
