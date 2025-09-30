
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.driver_setup import get_driver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.header_page import HeaderPage
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)



def test_orange_hrm():
    driver = get_driver()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(5)  # Let the login page load visibly

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    pim = PIMPage(driver)
    header = HeaderPage(driver)

    # Step 1: Login
    login.login("Admin", "admin123")
    time.sleep(5)  # Pause to show login success

    # Step 2: Add Employees
    employees = [
        ("Alice", "Smith", "E001"),
        ("Bob", "Brown", "E002"),
        ("Charlie", "Davis", "E003"),
        ("Zara", "Prince", "E004")
    ]

    for fname, lname, emp_id in employees:
        dashboard.go_to_pim()
        time.sleep(5)  # Pause before adding employee
        pim.add_employee(fname, lname, emp_id)
        time.sleep(5)  # Pause after adding employee

    # Step 3: Verify Employees
    for fname, lname, _ in employees:
        pim.verify_employee(f"{fname} {lname}")
        time.sleep(5)  # Pause after verification

    # Step 4: Logout
    header.logout()
    time.sleep(5)  # Pause to show logout

    driver.quit()

# Run the test
test_orange_hrm()