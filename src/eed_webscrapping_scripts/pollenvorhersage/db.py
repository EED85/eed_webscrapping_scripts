from eed_webscrapping_scripts.modules import connect_to_db
from eed_webscrapping_scripts.modules.duckdb_utils import add_primary_key


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
    if cfg["env"]["_ENVIRONMENT_"] == "PROD":
        con.sql("CREATE DATABASE IF NOT EXISTS pollenvorhersage")
    else:
        con.sql("ATTACH IF NOT EXISTS 'pollenvorhersage'")
    con.sql("USE pollenvorhersage")
    con.sql("CREATE SCHEMA IF NOT EXISTS datalake")
    con.sql("CREATE SCHEMA IF NOT EXISTS information_layer")
    con.sql(
        """
        CREATE TABLE IF NOT EXISTS datalake.saved_webpages(
            table_name VARCHAR PRIMARY KEY
            , inserttimestamptz TIMESTAMPTZ DEFAULT GET_CURRENT_TIMESTAMP()
        )
    """
    )

    con.sql(
        """
        CREATE TABLE IF NOT EXISTS information_layer.pollenflug_vorhersage(
            table_name VARCHAR
            , last_update TIMESTAMP
            , last_update_dt DATE
            , plz VARCHAR
            , pollenart VARCHAR
            , date DATE
            , inserttimestamptz TIMESTAMPTZ DEFAULT GET_CURRENT_TIMESTAMP()
        )
    """
    )

    add_primary_key(
        table_name="information_layer.pollenflug_vorhersage",
        primary_key=("last_update_dt", "plz", "pollenart", "date"),
        con=con,
        if_exists="pass",
    )

    return con
