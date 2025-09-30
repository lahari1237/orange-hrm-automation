import pytest
import time
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.driver_setup import get_driver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.header_page import HeaderPage

def generate_emp_id():
    return f"E{random.randint(1000, 9999)}"

@pytest.fixture(scope="module")
def setup():
    driver = get_driver()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(5)
    yield driver
    driver.quit()

def test_employee_workflow(setup):
    driver = setup
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    pim = PIMPage(driver)
    header = HeaderPage(driver)

    login.login("Admin", "admin123")
    time.sleep(5)

    employees = [
        ("Alice", "Smith", generate_emp_id()),
        ("Bob", "Brown", generate_emp_id()),
        ("Charlie", "Davis", generate_emp_id()),
        ("Zara", "Prince", generate_emp_id())
    ]

    for fname, lname, emp_id in employees:
        print(f"🆔 Using Employee ID: {emp_id}")
        dashboard.go_to_pim()
        pim.add_employee(fname, lname, emp_id)
        time.sleep(2)

    for fname, lname, _ in employees:
        pim.verify_employee(f"{fname} {lname}")
        time.sleep(2)

    header.logout()
    time.sleep(2)
