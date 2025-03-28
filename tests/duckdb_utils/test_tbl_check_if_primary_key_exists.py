from eed_webscrapping_scripts.modules import tbl_check_if_primary_key_exists


def test_tbl_check_if_primary_key_exists(cfg_test, prepare_db):
    con = prepare_db
    pk_exists = tbl_check_if_primary_key_exists(
        table_name="t01_primary_key", primapy_key=["id", "j"], con=con
    )
    assert pk_exists


def test_tbl_check_if_primary_key_not_exists(cfg_test, prepare_db):
    con = prepare_db
    pk_exists = tbl_check_if_primary_key_exists(
        table_name="t01_wo_primary_key", primapy_key=["id", "j"], con=con
    )
    assert not pk_exists
