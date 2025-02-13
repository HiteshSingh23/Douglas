import os
import shutil
import time
from datetime import datetime

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '0'

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import allure


@pytest.fixture(scope="session")
def browser():
    # Initialize the Chrome browser
    options = webdriver.ChromeOptions()
    # Suppress logs and errors
    options.add_argument('log-level=3')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("disable-infobars")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--disable-devtools")  # Suppress DevTools log

    global driver
    # Initialize the Chrome WebDriver with specified options
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    # Yield the driver to be used in tests
    yield driver

    # Cleanup after the tests are finished
    driver.quit()


"""allure report"""
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to get the test result
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Get the browser instance from the fixture
        driver = item.funcargs.get('browser', None)
        if driver:
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            screenshot_path = os.path.join(
                screenshot_dir,
                f"{item.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            )
            driver.save_screenshot(screenshot_path)

            # Attach the screenshot to the Allure report
            allure.attach.file(
                screenshot_path,
                name=f"Screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )
