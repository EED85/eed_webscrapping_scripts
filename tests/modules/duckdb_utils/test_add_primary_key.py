import pytest

from eed_webscrapping_scripts.modules import add_primary_key


@pytest.mark.parametrize(
    "table_name, primary_key, if_exists, primary_key_was_added_expected",
    [
        ("t01_primary_key", ["id", "j"], "pass", False),
        ("t01_wo_primary_key_add_pk", {"id", "j"}, "fail", True),
    ],
    ids=[
        "primary key already exists - fail safe - list as primary key",
        "primary key does not exists - set as primary key",
    ],
)
def test_add_primary_key(
    cfg_test, prepare_db, table_name, primary_key, if_exists, primary_key_was_added_expected
):
    con = prepare_db
    primary_key_was_added = add_primary_key(
        table_name=table_name, primary_key=primary_key, con=con, if_exists=if_exists
    )
    assert primary_key_was_added == primary_key_was_added_expected
