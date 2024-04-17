import pytest
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_inputs_from_file(file_path):
    input_data = {}
    with open(file_path, "r") as file:
        for line in file:
            # Ignore empty lines and lines starting with '#' (comments)
            if line.strip() == '' or line.strip().startswith('#'):
                continue
            # Split the line into key and value by the first '='
            parts = line.split('=', 1)
            # Ensure there are exactly two parts
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                input_data[key] = value
            else:
                print(f"Ignore invalid line: {line.strip()}")
    return input_data


@pytest.fixture(scope="module")
def browser():
    # Initialize Safari WebDriver
        driver = webdriver.Safari()
        return driver


def test_admin_login(browser):
    # Retrieve admin credentials from command line
    inputs = read_inputs_from_file('input_file.txt')
    login_page_url = inputs["login_page_url"]
    main_page_url = inputs["main_page_url"]
    admin_username = inputs["admin_username"]
    admin_password = inputs["admin_password"]

    browser.get(login_page_url)

    username_input = browser.find_element(By.ID, 'email')
    password_input = browser.find_element(By.ID, 'password')
    username_input.send_keys(admin_username)
    password_input.send_keys(admin_password)
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    status_code = browser.execute_script("""
    var xhr = new XMLHttpRequest();
    xhr.open('GET', arguments[0], false);  // Synchronous request
    xhr.send(null);
    return xhr.status;
    """, browser.current_url)

    assert status_code == 200, f"Expected status code 200, but got {status_code}"


if __name__ == '__main__':
    pytest.main()

