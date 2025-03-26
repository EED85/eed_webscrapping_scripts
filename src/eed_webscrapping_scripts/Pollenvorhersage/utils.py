import os

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from eed_webscrapping_scripts.modules import get_git_root, load_dotenv_


def get_config() -> dict:
    """Generates a dict based on ``config.yaml``.
    These parameters are used in the whole programm to pass Variables between programms.

    Returns:
        dict: _description_
    """
    cfg = {}
    git_root = get_git_root() / "src" / "eed_webscrapping_scripts"
    path_to_config = git_root / "Pollenvorhersage" / "config.yaml"
    runs_on_ga = os.getenv("RUNS_ON_GA") or "0"
    if not int(runs_on_ga):
        load_dotenv_()

    with open(path_to_config) as file:
        cfg = yaml.safe_load(file)
    cfg["git_root"] = git_root
    cfg["env"]["_ENVIRONMENT_"] = os.getenv("_ENVIRONMENT_")
    cfg["runs_on_ga"] = cfg["env"]["_ENVIRONMENT_"] == "GITHUB"
    return cfg


def open_webpage_and_select_plz(url, plz, driver=None):
    if driver is None:
        driver = webdriver.Chrome()
    driver.get(url)
    # Find the search box using XPath
    search_box = driver.find_element(By.XPATH, '//*[@id="searchBox"]')
    search_box.send_keys(plz)
    search_box.send_keys(Keys.RETURN)
    return driver


def upload_webpage_to_db(con, file, cfg):
    con.sql(f"""
        CREATE OR REPLACE TEMP TABLE _webpage_ AS
        SELECT
            parse_filename(filename) AS file,
            content,
            size,
            last_modified,
            last_modified::DATE AS last_modified_date,
        FROM read_blob('{str(cfg["git_root"])}\**')
        WHERE TRUE
            AND filename = '{str(file)}'
    """)

    con.sql("""CREATE TABLE IF NOT EXISTS datalake.webpages AS SELECT * FROM _webpage_ LIMIT 0""")

    # con.sql(
    #     "FROM duckdb_constraints()
    #   SELECT * EXCLUDE(database_name, schema_oid, database_oid, table_oid,
    # constraint_index, constraint_name)
    # WHERE constraint_type = 'PRIMARY KEY'"
    # )
    con.sql("""
            SELECT IF(COUNT(*)=0, FALSE, TRUE)
            FROM duckdb_constraints()
            WHERE TRUE
                AND table_name = 'webpages'
                AND schema_name = 'datalake'
                AND constraint_column_names = ['file', 'last_modified_date']
    """)
    con.sql("""
        ALTER TABLE datalake.webpages
        ADD PRIMARY KEY (file, last_modified_date);""")
    pass
