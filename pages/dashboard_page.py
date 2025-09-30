from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.pim_menu = (By.XPATH, "//span[text()='PIM']")
        self.dashboard_header = (By.XPATH, "//h6[text()='Dashboard']")

    def go_to_pim(self):
        # Wait for dashboard to fully load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.dashboard_header)
        )

        try:
            # Wait for PIM menu to be visible
            pim = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.pim_menu)
            )
            pim.click()
        except Exception as e:
            print("Error locating or clicking PIM menu:", e)
            print("Page source for debugging:\n", self.driver.page_source)
            raise
