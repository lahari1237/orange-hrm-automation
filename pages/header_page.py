from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HeaderPage:
    def __init__(self, driver):
        self.driver = driver
        self.profile_icon = (By.CLASS_NAME, "oxd-userdropdown-name")
        self.logout_link = (By.XPATH, "//a[text()='Logout']")

    def logout(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.profile_icon)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.logout_link)).click()