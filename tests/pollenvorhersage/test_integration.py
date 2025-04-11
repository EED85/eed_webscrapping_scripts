from pathlib import Path

from eed_webscrapping_scripts.pollenvorhersage.pollenvorhersage import pollenvorhersage


def test_pollenvorhersage(cfg_test):
    con = pollenvorhersage()
    con.sql("SELECT 1 AS ONE")
    con.close()
    Path.unlink("pollenvorhersage.duckdb")
    assert True
