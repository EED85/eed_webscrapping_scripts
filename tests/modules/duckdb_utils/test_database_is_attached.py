import pytest

from eed_webscrapping_scripts.modules import datatbase_is_attached


@pytest.mark.parametrize(
    "database_name, expected",
    [
        ("attached_db", True),
        ("non_attached_db", False),
    ],
    ids=["attached_db", "non_attached_db"],
)
def test_datatbase_is_attached(cfg_test, prepare_db, database_name, expected):
    con = prepare_db
    if database_name == "attached_db":
        database_name_to_check = cfg_test["db"]["database"]
    else:
        database_name_to_check = database_name
    db_is_attached = datatbase_is_attached(database_name_to_check, con)

    assert db_is_attached == expected
