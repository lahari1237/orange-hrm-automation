from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.NAME, "username")
        self.password = (By.NAME, "password")
        self.login_btn = (By.XPATH, "//button[@type='submit']")

    def login(self, user, pwd):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.username)).send_keys(user)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.password)).send_keys(pwd)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.login_btn)).click()