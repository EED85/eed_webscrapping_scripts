from eed_webscrapping_scripts.dwd import prepare_db
from eed_webscrapping_scripts.dwd import download_json_to_duckdb
from eed_webscrapping_scripts.dwd import get_config


def pollenflug_gefahrenindex():
    print("START pollenflug_gefahrenindex")
    config = get_config()
    url = config["pollenflug_gefahrenindex"]["url"]
    con = prepare_db()
    download_json_to_duckdb(url, con)
    print("ENDE pollenflug_gefahrenindex")


if __name__ == "__main__":
    pollenflug_gefahrenindex()
