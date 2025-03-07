def test_package_import(get_config_test):
    import eed_webscrapping_scripts

    print(eed_webscrapping_scripts.__path__)
    assert True
