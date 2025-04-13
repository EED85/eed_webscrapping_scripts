import os

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from eed_webscrapping_scripts.modules import (
    add_primary_key,
    get_git_root,
    get_table_definition,
    load_dotenv_,
    sleep_random,
)


def get_environment() -> str:
    load_dotenv_()

    _EXECUTION_MODE_ = os.getenv("_EXECUTION_MODE_")
    _EXECUTION_ENVIRONMENT_ = os.getenv("_EXECUTION_ENVIRONMENT_")

    if _EXECUTION_MODE_ == "IDE" and _EXECUTION_ENVIRONMENT_ == "local":
        return "PROD"
    elif (_EXECUTION_MODE_ == "PYTEST" and _EXECUTION_ENVIRONMENT_ == "local") or (
        _EXECUTION_MODE_ == "PYTEST" and _EXECUTION_ENVIRONMENT_ == "GITHUB"
    ):
        return "DEV"
    elif _EXECUTION_MODE_ == "GA" and _EXECUTION_ENVIRONMENT_ == "GITHUB":
        return "PROD"
    else:
        raise ValueError(
            f"No enviroment specified for {_EXECUTION_MODE_=}, {_EXECUTION_ENVIRONMENT_=}"
        )


def get_config() -> dict:
    """Generates a dict based on ``config.yaml``.
    These parameters are used in the whole programm to pass Variables between programms.

    Returns:
        dict: _description_
    """
    cfg = {}
    git_root = get_git_root() / "src" / "eed_webscrapping_scripts"
    path_to_config = git_root / "pollenvorhersage" / "config.yaml"
    with open(path_to_config) as file:
        cfg = yaml.safe_load(file)

    _ENVIRONMENT_ = get_environment()
    cfg["git_root"] = git_root
    cfg["env"]["_EXECUTION_ENVIRONMENT_"] = os.getenv("_EXECUTION_ENVIRONMENT_")
    cfg["env"]["_ENVIRONMENT_"] = _ENVIRONMENT_
    cfg["env"]["_EXECUTION_MODE_"] = os.getenv("_EXECUTION_MODE_")
    cfg["runs_on_ga"] = cfg["env"]["_EXECUTION_ENVIRONMENT_"] == "GITHUB"
    return cfg


def open_webpage_and_select_plz(url, plz, driver=None):
    if driver is None:
        driver = webdriver.Chrome()
    driver.get(url)
    sleep_random(1, 2)
    # Find the search box using XPath
    search_box = driver.find_element(By.XPATH, '//*[@id="searchBox"]')
    search_box.send_keys(plz)
    search_box.send_keys(Keys.RETURN)
    return driver


def upload_webpage_to_db(con, file, plz, cfg: dict, table: str = "_webpage_"):
    con.sql(f"""
        CREATE OR REPLACE TEMP TABLE {table} AS
        SELECT
            parse_filename(filename) AS file,
            content,
            size,
            '{plz}' AS plz,
            last_modified,
            last_modified::DATE AS last_modified_date,
        FROM read_text('{str(file)}')
        WHERE TRUE
    """)
    table_webpages = get_table_definition(cfg=cfg, table_name="webpages")
    con.sql(
        f"""CREATE TABLE IF NOT EXISTS {table_webpages["path"]} AS SELECT * FROM {table} LIMIT 0"""
    )
    add_primary_key(
        table_name=table_webpages["path"],
        primary_key=table_webpages["primary_key"],
        con=con,
        if_exists="pass",
    )
    con.sql(f"""
        INSERT OR IGNORE INTO {table_webpages["path"]}
        SELECT * FROM {table}
    """)

    pass
