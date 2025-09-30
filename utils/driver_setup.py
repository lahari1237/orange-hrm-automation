from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Use the full path to your extracted ChromeDriver
    service = Service("C:\\WebDrivers\\chromedriver-win32\\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    return driver