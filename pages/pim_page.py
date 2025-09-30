from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_btn = (By.XPATH, "//button[text()=' Add ']")
        self.first_name = (By.NAME, "firstName")
        self.last_name = (By.NAME, "lastName")
        self.employee_id = (By.XPATH, "//label[text()='Employee Id']/following::input[1]")
        self.save_btn = (By.XPATH, "//button[@type='submit']")
        self.success_toast = (By.CLASS_NAME, "oxd-toast")
        self.employee_name_input = (By.XPATH, "//input[@placeholder='Type for hints...']")
        self.search_btn = (By.XPATH, "//button[@type='submit' and contains(@class,'oxd-button--secondary')]")

    def add_employee(self, fname, lname, emp_id=None):
        try:
            current_url = self.driver.current_url
            if "viewPersonalDetails" in current_url:
                print("⚠️ Still on personal details page. Navigating back to PIM.")
                self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
                time.sleep(2)

            print("Clicking Add button...")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_btn)).click()
            time.sleep(2)

            print("Entering first and last name...")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.first_name)).send_keys(fname)
            self.driver.find_element(*self.last_name).send_keys(lname)
            time.sleep(2)

            if emp_id:
                if len(emp_id) > 10:
                    print(f"⚠️ Employee ID '{emp_id}' exceeds 10 characters. Truncating.")
                    emp_id = emp_id[:10]

                print(f"Clearing and entering Employee ID: {emp_id}")
                emp_id_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.employee_id))
                emp_id_field.send_keys(Keys.CONTROL + "a")
                emp_id_field.send_keys(Keys.DELETE)
                emp_id_field.send_keys(emp_id)
                time.sleep(2)

                actual_id = emp_id_field.get_attribute("value")
                if len(actual_id) > 10:
                    print(f"❌ Employee ID still exceeds 10 characters: {actual_id}")
                    self.driver.save_screenshot(f"invalid_emp_id_{fname}_{lname}.png")
                    return

            print("Clicking Save button...")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.save_btn)).click()
            time.sleep(2)

            print("Waiting for success toast...")
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.success_toast))
                print("✅ Employee added successfully!")
            except Exception:
                print("❌ Success toast not found. Possible validation error.")
                self.driver.save_screenshot(f"toast_missing_{fname}_{lname}.png")
                raise

            time.sleep(2)

        except Exception as e:
            print(f"❌ Error while adding employee: {e}")
            self.driver.save_screenshot(f"add_employee_error_{fname}_{lname}.png")
            raise

    def verify_employee(self, name):
        try:
            print("Navigating to Employee List...")
            self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
            time.sleep(2)

            print(f"Searching for employee: {name}")
            name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.employee_name_input)
            )
            name_input.clear()
            name_input.send_keys(name)
            time.sleep(1)
            name_input.send_keys(Keys.ARROW_DOWN)
            name_input.send_keys(Keys.ENTER)
            time.sleep(2)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.search_btn)
            ).click()
            time.sleep(2)

            print("Waiting for table to load...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "oxd-table-body"))
            )
            time.sleep(2)

            print("Checking rows for employee match...")
            first_name, last_name = name.split(" ", 1)
            found = False

            rows = self.driver.find_elements(By.CLASS_NAME, "oxd-table-row")
            for i, row in enumerate(rows):
                try:
                    cells = row.find_elements(By.CLASS_NAME, "oxd-table-cell")
                    cell_texts = [cell.text.strip() for cell in cells]
                    print(f"Row {i} contents: {cell_texts}")
                    if first_name in cell_texts and last_name in cell_texts:
                        found = True
                        break
                except Exception as inner:
                    print(f"Skipping stale row {i}: {inner}")
                    continue

            screenshot_name = f"verify_{'success' if found else 'error'}_{name.replace(' ', '_')}.png"
            self.driver.save_screenshot(screenshot_name)

            if found:
                print(f"✅ {name} Verified in employee list.")
            else:
                print(f"❌ {name} not found in employee list.")

            time.sleep(2)

        except Exception as e:
            print(f"❌ Error while verifying employee: {e}")
            self.driver.save_screenshot(f"verify_error_{name.replace(' ', '_')}.png")
            raise
