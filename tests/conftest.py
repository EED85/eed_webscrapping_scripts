import os
from collections.abc import Iterator
from pathlib import Path

import duckdb
import pytest
import yaml

from eed_webscrapping_scripts.modules import get_encryption_pasword


def get_encryption_result(home_dir) -> bytes:
    """Reads password either from disk or from a github secret.

    Args:

    Returns:
        str: password -> use it in functions encrypt and decrypt
    """
    try:
        with open(os.path.join(home_dir, ".encryption_result")) as f:
            encryption_result = f.read()
    except Exception:
        encryption_result = os.getenv("ENCRYPTION_RESULT")
    return bytes(encryption_result.strip(), encoding="utf-8")


# Fixture to use the mock_load_config function
@pytest.fixture(scope="session")
def patch_get_config_dwd(monkeypatch):
    def get_config_dwd_mock():
        with open(Path("tests") / "dwd" / "config.yaml") as file:
            return yaml.safe_load(file)

    monkeypatch.setattr("eed_webscrapping_scripts.dwd.get_config", get_config_dwd_mock)


@pytest.fixture(scope="session")
def db_setup():
    con = duckdb.connect()
    yield con


@pytest.fixture(scope="session")
def cfg_test(db_setup) -> Iterator[dict]:
    home_dir = os.path.expanduser("~")
    password = get_encryption_pasword()
    encryption_result = get_encryption_result(home_dir)
    cfg_test = {
        "home_dir": home_dir,
        "encrytpion": {"password": password, "result": encryption_result},
        "db": {
            "con": db_setup,
            "database": "db_test",
            "schema": "schema_test",
        },
    }
    yield cfg_test


@pytest.fixture(scope="session")
def prepare_db(cfg_test: dict):
    con = cfg_test["db"]["con"]
    database = cfg_test["db"]["database"]
    schema = cfg_test["db"]["schema"]

    con.sql(f"""ATTACH IF NOT EXISTS '{database}.duckdb'""")
    con.sql(f"""USE {database}""")
    con.sql(f"""CREATE SCHEMA IF NOT EXISTS {schema}""")
    con.sql(f"""USE {schema}""")

    # prepare tables for testing
    con.sql("""
        CREATE OR REPLACE TABLE t01_primary_key (id INTEGER, j VARCHAR, PRIMARY KEY (id, j));
        CREATE OR REPLACE TABLE t01_wo_primary_key (id INTEGER, j VARCHAR);
    """)
    yield con
    con.close()
    Path.unlink(f"{database}.duckdb")
