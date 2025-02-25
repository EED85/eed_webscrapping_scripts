import os
import duckdb

home_dir = os.path.expanduser("~")


def prepare_db():
    try:
        with open(os.path.join(home_dir, ".motherduck_token")) as f:
            md_token = f.read()
    except Exception:
        md_token = os.getenv("MD_TOKEN")

    con = duckdb.connect(f"md:?motherduck_token={md_token.strip()}")
    con.sql("CREATE DATABASE IF NOT EXISTS dwd")
    con.sql("USE dwd")
    con.sql("CREATE SCHEMA IF NOT EXISTS datalake")
    con.sql(
        """
        CREATE TABLE IF NOT EXISTS datalake.loaded_tables(table_name VARCHAR PRIMARY KEY, last_update timestamp, inserttimestamptz TIMESTAMPTZ DEFAULT GET_CURRENT_TIMESTAMP());
    """
    )
    return con
