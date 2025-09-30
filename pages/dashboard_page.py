from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        # Updated locator using href for better stability
        self.pim_menu = (By.CSS_SELECTOR, "a[href='/web/index.php/pim/viewPimModule']")
        self.app_container = (By.ID, "app")  # Confirms page has rendered

    def go_to_pim(self):
        # Wait for the app container to confirm page load
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.app_container)
        )

        try:
            # Wait for the PIM menu to be visible and click it
            pim = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.pim_menu)
            )
            pim.click()
        except Exception as e:
            print("Error locating or clicking PIM menu:", e)
            print("Page source for debugging:\n", self.driver.page_source)
            raise
