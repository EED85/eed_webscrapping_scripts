from pathlib import Path

from eed_webscrapping_scripts.pollenvorhersage.pollenvorhersage import PollenvorhersageHandler


def test_pollenvorhersage(cfg_test):
    pollenvorhersage_handler = PollenvorhersageHandler()
    con = pollenvorhersage_handler.fetch_and_store_html()
    pollenvorhersage_handler.extract_pollenvorhersage()
    con.sql("SELECT 1 AS ONE")
    con.close()
    Path.unlink("pollenvorhersage.duckdb")
    assert True
