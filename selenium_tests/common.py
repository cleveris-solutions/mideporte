import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv


def initialize_driver():
    load_dotenv()
    # Initializes the browser options
    options = webdriver.ChromeOptions()

    # Initialise the browser using WebDriver Manager
    service = Service(os.getenv("CHROMEDRIVER_BIN_PATH"))
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def close_driver(driver):
    driver.quit()
