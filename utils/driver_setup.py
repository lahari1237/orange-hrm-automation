from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_driver(options=None):
    service = Service("C:\\WebDrivers\\chromedriver-win32\\chromedriver.exe")  # Update with your actual path
    return webdriver.Chrome(service=service, options=options)

