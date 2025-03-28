import time
from pathlib import Path

from selenium import webdriver

from eed_webscrapping_scripts.modules import decrypt_direct, save_webpage
from eed_webscrapping_scripts.Pollenvorhersage import (
    get_config,
    open_webpage_and_select_plz,
    prepare_db,
    upload_webpage_to_db,
)

# Initialize the WebDriver


def pollenvorhersage():
    print("START")

    # set parameters
    cfg = get_config()
    url = decrypt_direct(cfg["pollenvorhersage"]["url"])
    plzs = [decrypt_direct(plz) for plz in cfg["pollenvorhersage"]["plz"]]
    driver = webdriver.Chrome()

    con = prepare_db(cfg)

    for _i_, plz in enumerate(plzs):
        driver = open_webpage_and_select_plz(url, plz, driver)
        time.sleep(2.5)
        file_rel = Path("Pollenvorhersage", "websites", f"{str(_i_).zfill(5)}.html")
        file = Path(cfg["git_root"], file_rel)
        save_webpage(driver.page_source, str(file))
        upload_webpage_to_db(con, file, cfg)

    # Enter the value into the search box

    # soup.find_all('img', {'title': True})
    # soup.find_all(class_='datum')
    # soup.find_all(class_='tooltip')

    # Wait for the data to load and scrape the data
    # Add your scraping logic here

    # Close the WebDriver
    driver.quit()
    print("END")


if __name__ == "__main__":
    pollenvorhersage()
