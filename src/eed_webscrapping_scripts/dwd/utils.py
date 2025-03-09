import os

import yaml

from eed_webscrapping_scripts.modules import get_git_root, load_dotenv_


def download_json_to_duckdb(url: str, con):
    """Downloads json form the api ``url``.
    Creates a table ``Pollenflug_Gefahrenindex_{date}``.
    Loggs the download in the table ``loaded_tables``.
    Args:
        url (str): _description_
        con (Duckdb / Motherduck connection): Needs to have dwd has current database,
    """
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
        f"""INSERT OR IGNORE INTO datalake.loaded_tables(table_name, last_update)
            VALUES('{table_name}', '{_last_update}')
        ;"""
    )


def get_config() -> dict:
    """Generates a dict based on ``config.yaml``.
    These parameters are used in the whole programm to pass Variables between programms.

    Returns:
        dict: _description_
    """
    cfg = {}
    git_root = get_git_root() / "src" / "eed_webscrapping_scripts"
    path_to_config = git_root / "dwd" / "config.yaml"
    runs_on_ga = os.getenv("RUNS_ON_GA") or "0"
    if not int(runs_on_ga):
        load_dotenv_()

    with open(path_to_config) as file:
        cfg = yaml.safe_load(file)
    cfg["git_root"] = git_root
    cfg["env"]["_ENVIRONMENT_"] = os.getenv("_ENVIRONMENT_")
    print(f"""{cfg["env"]["_ENVIRONMENT_"]=}""")
    return cfg
