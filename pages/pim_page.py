from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_btn = (By.XPATH, "//button[text()=' Add ']")
        self.first_name = (By.NAME, "firstName")
        self.last_name = (By.NAME, "lastName")
        self.employee_id = (By.XPATH, "//*[@id='app']/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/input")
        self.save_btn = (By.XPATH, "//button[@type='submit']")
        self.success_toast = (By.XPATH, "//div[contains(@class,'oxd-toast-content')]")

        # Correct locators for Employee Information search
        self.employee_name_input = (By.XPATH, "//input[@placeholder='Type for hints...']")
        self.search_btn = (By.XPATH, "//button[@type='submit' and contains(@class,'oxd-button--secondary')]")

    def add_employee(self, fname, lname, emp_id=None):
        try:
            print("Clicking Add button...")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_btn)).click()

            print("Entering first and last name...")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.first_name)).send_keys(fname)
            self.driver.find_element(*self.last_name).send_keys(lname)

            if emp_id:
                print(f"Entering Employee ID: {emp_id}")
                emp_id_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.employee_id))
                emp_id_field.clear()
                emp_id_field.send_keys(emp_id)

            print("Clicking Save button...")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.save_btn)).click()

            print("Waiting for success toast...")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.success_toast)
            )
            print("Employee added successfully!")

        except Exception as e:
            print(f" Error while adding employee: {e}")
            self.driver.save_screenshot("add_employee_error.png")
            raise

    def verify_employee(self, name):
        try:
            print("Navigating to Employee List...")
            self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")

            print(f"Searching for employee: {name}")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.employee_name_input)).send_keys(name)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.search_btn)).click()

            print("Waiting for table to load...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "oxd-table-body"))
            )

            print("Checking rows for employee match...")
            rows = self.driver.find_elements(By.CLASS_NAME, "oxd-table-row")
            first_name, last_name = name.split(" ", 1)
            found = False

            for row in rows:
                cells = row.find_elements(By.CLASS_NAME, "oxd-table-cell")
                cell_texts = [cell.text.strip() for cell in cells]
                if first_name in cell_texts and last_name in cell_texts:
                    found = True
                    break

            if found:
                print(f" {name} Verified in employee list.")
            else:
                print(f" {name} not found in employee list.")
                self.driver.save_screenshot(f"verify_error_{name.replace(' ', '_')}.png")

        except Exception as e:
            print(f" Error while verifying employee: {e}")
            self.driver.save_screenshot(f"verify_error_{name.replace(' ', '_')}.png")
            raise