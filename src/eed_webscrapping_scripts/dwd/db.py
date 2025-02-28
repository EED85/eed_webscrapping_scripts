from eed_webscrapping_scripts.modules import connect_to_db


def prepare_db(con=None):
    con = con or connect_to_db()
    con.sql("CREATE DATABASE IF NOT EXISTS dwd")
    con.sql("USE dwd")
    con.sql("CREATE SCHEMA IF NOT EXISTS datalake")
    con.sql(
        """
        CREATE TABLE IF NOT EXISTS datalake.loaded_tables(table_name VARCHAR PRIMARY KEY, last_update timestamp, inserttimestamptz TIMESTAMPTZ DEFAULT GET_CURRENT_TIMESTAMP());
    """
    )
    return con
