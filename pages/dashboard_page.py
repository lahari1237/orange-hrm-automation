from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.pim_menu = (By.XPATH, "//span[text()='PIM']")

    def go_to_pim(self):
        pim = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.pim_menu))
        ActionChains(self.driver).move_to_element(pim).click().perform()