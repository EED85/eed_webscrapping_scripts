import pytest

from eed_webscrapping_scripts.modules import check_if_primary_key_exists


@pytest.mark.parametrize(
    "table_name, primary_key_exists",
    [
        ("t01_primary_key", True),
        ("t01_wo_primary_key", False),
    ],
    ids=[
        "primary key exists - list as primary key",
        "primary key does not exists - set as primary key",
    ],
)
def test_check_if_primary_key_exists(cfg_test, prepare_db, table_name, primary_key_exists):
    con = prepare_db
    pk_exists = check_if_primary_key_exists(table_name=table_name, con=con)
    assert pk_exists == primary_key_exists
