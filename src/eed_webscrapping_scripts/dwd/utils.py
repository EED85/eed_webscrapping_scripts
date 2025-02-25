import eed_webscrapping_scripts
import os
import yaml


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


def get_config():
    path_to_config = os.path.join(
        eed_webscrapping_scripts.__path__[0], "dwd", "config.yaml"
    )

    with open(path_to_config, "r") as file:
        cfg = yaml.safe_load(file)
    return cfg


if __name__ == "__main__":
    get_config()
