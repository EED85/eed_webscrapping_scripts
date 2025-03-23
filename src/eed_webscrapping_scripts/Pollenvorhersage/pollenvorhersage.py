import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize the WebDriver


def pollenvorhersage():
    print("START")
    driver = webdriver.Chrome()

    driver.get("")

    # Find the search box using XPath
    search_box = driver.find_element(By.XPATH, '//*[@id="searchBox"]')

    # Enter the value into the search box
    search_box.send_keys("00000")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2.5)
    # soup.find_all('img', {'title': True})
    # soup.find_all(class_='datum')
    # soup.find_all(class_='tooltip')

    soup = BeautifulSoup(driver.page_source, "html.parser")
    with open("webpage.html", "w") as f:
        f.write(str(soup.prettify().encode("utf-8", "ignore")))

    # Wait for the data to load and scrape the data
    # Add your scraping logic here

    # Close the WebDriver
    driver.quit()
    print("END")


if __name__ == "__main__":
    pollenvorhersage()
