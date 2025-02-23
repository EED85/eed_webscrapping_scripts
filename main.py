import duckdb
import os

home_dir = os.path.expanduser("~")


def download_json_to_duckdb(url, con):

    sql_date = f"""
                WITH _date AS (
                    SELECT
                        MAX(strptime(last_update, '%Y-%m-%d %H:%M Uhr')) AS last_update
                    FROM read_json('{url}')
                )
                SELECT strftime(last_update, '%Y-%m-%d %H:%M:%S')
                        , strftime(last_update, '%Y_%m_%d')
                        -- , last_update
                FROM _date
    """

    _last_update, _date = con.sql(sql_date).fetchone()
    table_name = f"Pollenflug_Gefahrenindex_{_date}"
    con.sql(
        f"""
        CREATE TABLE IF NOT EXISTS datalake.{table_name} AS FROM read_json('{url}');
    """
    )
    con.sql(
        f"INSERT OR IGNORE INTO datalake.loaded_tables(table_name, last_update) VALUES('{table_name}', '{_last_update}');"
    )


def prepare_db():
    try:
        with open(os.path.join(home_dir, ".motherduck_token")) as f:
            md_token = f.read()
    except Exception:
        md_token = os.getenv('MD_TOKEN')

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


def save_database():
    pass


def main():
    url = "https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json"
    con = prepare_db()
    print("Hello from eed-webscrapping-scripts!")
    download_json_to_duckdb(url, con)
    save_database()


if __name__ == "__main__":
    main()
