import re
from datetime import datetime
from pathlib import Path

import polars as pl
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium import webdriver

from eed_webscrapping_scripts.modules import (
    ask_user_for_local_production_run,
    create_table_from_lists,
    decode_string,
    decrypt_direct,
    decrypt_file,
    save_webpage,
)
from eed_webscrapping_scripts.pollenvorhersage import (
    download_wepages,
    get_config,
    open_webpage_and_select_plz,
    prepare_db,
    upload_webpage_to_db,
)


class PollenvorhersageHandler:
    def __init__(self):
        self.cfg = get_config()
        self.con = prepare_db(self.cfg)

    def fetch_and_store_html(self):
        print("START")

        # set parameters
        cfg = self.cfg
        ask_user_for_local_production_run(cfg)
        url = decrypt_direct(cfg["pollenvorhersage"]["url"])
        plzs = [decrypt_direct(plz) for plz in cfg["pollenvorhersage"]["plz"]]
        print(len(plzs))

        con = self.con

        for _i_, plz in enumerate(plzs):
            print(f"{_i_=}")
            if cfg["env"]["_ENVIRONMENT_"] == "PROD":
                driver = webdriver.Chrome()
                driver = open_webpage_and_select_plz(url, plz, driver)
                file_rel = Path("pollenvorhersage", "websites", f"{plz}.html")
                file = Path(cfg["git_root"], file_rel)
                save_webpage(driver.page_source, str(file))
            else:
                # do not access website, use encrypted webpage instead
                file_rel_encrypted = Path("pollenvorhersage", "websites", "encrypted_website.html")
                file_encrypted = Path(cfg["git_root"], file_rel_encrypted)
                file_rel_decrypted = Path("pollenvorhersage", "websites", "decrypted_website.html")
                file = Path(cfg["git_root"], file_rel_decrypted)
                decrypt_file(file_encrypted, file)

            upload_webpage_to_db(con, file, plz, cfg)
            print("upladed")

        # clean up
        match cfg["env"]["_ENVIRONMENT_"]:
            case "PROD":
                driver.quit()
                con.close()
            case "DEV":
                pass

        print("END")
        return con

    def extract_pollenvorhersage(self):
        cfg = self.cfg
        con = self.con
        webpages = download_wepages(cfg=cfg, con=con)
        print(webpages)

        current_date = datetime.now().date()
        for i in range(len(webpages)):
            content = webpages["content"][i]
            soup = BeautifulSoup(content, "html.parser")
            dates_to_extract = soup.find_all(class_="datum")
            dates = list(range(len(dates_to_extract)))
            for j in range(len(dates_to_extract)):
                date_to_extract = dates_to_extract[j].get_text(strip=True)
                dd_mm = re.search(r"\d{2}.\d{2}", date_to_extract)[0]
                parsed_date = parse(f"""{dd_mm}.{current_date.year}""", dayfirst=True).date()
                dates[j] = parsed_date
            dates_str = [date.strftime("%Y_%m_%d") for date in dates]
            soup_pollenarten = soup.find_all(class_="tooltip")
            pollenarten = list(range(len(soup_pollenarten)))
            for k in range(len(soup_pollenarten)):
                pollenart = soup_pollenarten[k].find(class_="tooltiptext").find("img")["alt"]
                pollenarten[k] = decode_string(pollenart)

            soup_belastungen = soup.find_all("img", {"title": True})
            belastungen = [
                belastung["title"]
                for belastung in soup_belastungen[: (len(dates) * len(soup_pollenarten))]
            ]

            df = create_table_from_lists(
                column_names=dates_str,
                values=belastungen,
                row_indices=pollenarten,
                row_indices_column_name="pollenart",
            )
            df = df.unpivot(index="pollenart")

            # TODO: Encoding using polars does not work yet, normla function works
            df = df.with_columns(
                pl.col("pollenart")
                .map_elements(lambda x: decode_string(x))
                .alias("pollenart_decoded")
            )

            print(len(df))
            mapping = {
                "keine Belastung": 0,
                "schwache Belastung": 1,
                "mittlere Belastung": 2,
                "starke Belastung": 3,
            }
            con.sql(f"""
                -- CREATE OR REPLACE TEMP TABLE pollenflug AS
                SELECT
                    * EXCLUDE(variable)
                    , strptime(variable, '%Y_%m_%d')::DATE AS date
                    , MAP {str(mapping)}[value] AS belastung
                FROM df
                WHERE pollenart = 'Gräser'
                ORDER BY pollenart, date
            """)
        # Wait for the data to load and scrape the data
        # Add your scraping logic here


if __name__ == "__main__":
    pollenvorhersage_handler = PollenvorhersageHandler()
    con = pollenvorhersage_handler.fetch_and_store_html()
