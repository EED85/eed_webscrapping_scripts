from eed_webscrapping_scripts.pollenvorhersage import pollenvorhersage


def test_pollenvorhersage(cfg_test):
    con = pollenvorhersage()
    con.sql("SELET 1 AS ONE")
    assert True
