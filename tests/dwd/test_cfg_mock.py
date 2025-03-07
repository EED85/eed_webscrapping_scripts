def test_mocking(patch_get_config_dwd):
    from eed_webscrapping_scripts.dwd import get_config

    cfg = get_config()
    assert not cfg["pollenflug_gefahrenindex"]["url"].startswith("https://opendata.dwd.de/")
