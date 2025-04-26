from pathlib import Path

from selenium import webdriver

from eed_webscrapping_scripts.modules import (
    ask_user_for_local_production_run,
    decrypt_direct,
    decrypt_file,
    save_webpage,
)
from eed_webscrapping_scripts.pollenvorhersage import (
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

        # Enter the value into the search box

        # soup.find_all('img', {'title': True})
        # soup.find_all(class_='datum')
        # soup.find_all(class_='tooltip')

        # Wait for the data to load and scrape the data
        # Add your scraping logic here

        # clean up

        match cfg["env"]["_ENVIRONMENT_"]:
            case "PROD":
                driver.quit()
                con.close()
            case "DEV":
                pass

        print("END")
        return con


if __name__ == "__main__":
    pollenvorhersage_handler = PollenvorhersageHandler()
    con = pollenvorhersage_handler.fetch_and_store_html()
    con.close()
