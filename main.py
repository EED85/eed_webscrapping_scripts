import duckdb


def download_json_to_duckdb(url, con):
    con.sql(f"""
        CREATE OR REPLACE TABLE data AS FROM read_json('{url}');
    """)

def main():
    url = 'https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json'
    con = duckdb.connect('dwd.duckdb')
    print("Hello from eed-webscrapping-scripts!")
    download_json_to_duckdb(url, con)


if __name__ == "__main__":
    main()
