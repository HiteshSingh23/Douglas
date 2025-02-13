import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from resources import variables
from resources.utils import read_xlsx_column_by_name  # Import utility to read Excel
from pages.basePage import BasePage


class Perfum(BasePage):
    SHADOW_HOST_LOCATOR = (By.ID, "usercentrics-root")
    ACCEPT_BUTTON_SELECTOR = "[data-testid='uc-accept-all-button']"
    PERFUME_LOCATOR = (By.XPATH, "//li[@aria-label='PARFUM']")
    OPEN_DROPDOWN = (By.XPATH, "//div[@class='facet__title' and contains(text(),'Aktionen')]")

    def load_url(self):
        self.browser.get(variables.url)
        time.sleep(5)

    def accept_cookies(self):
        accept_button = self.find_shadow_element(self.SHADOW_HOST_LOCATOR, self.ACCEPT_BUTTON_SELECTOR)
        accept_button.click()

    def click_perfume(self):
        self.click(self.PERFUME_LOCATOR)
        time.sleep(15)

    def apply_filters(self, file_path, column_name):
        # Read filter values from Excel
        filter_values = read_xlsx_column_by_name(file_path, column_name)

        for filter_text in filter_values:
            # Open the dropdown for each filter value
            self.click(self.OPEN_DROPDOWN)
            time.sleep(2)

            try:
                # Dynamically generate XPath with the filter value
                dynamic_xpath = f"//div[@class='facet-option__label']/div[contains(text(),'{filter_text.strip()}')]"

                # Wait for the element to appear
                filter_element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, dynamic_xpath))
                )

                # Scroll the element into view
                self.browser.execute_script("arguments[0].scrollIntoView(true);", filter_element)
                time.sleep(1)  # Allow scrolling to complete

                # Click the filter element
                filter_element.click()
                time.sleep(10)  # Allow the filter to be applied
            except Exception as e:
                print(f"Filter '{filter_text}' not found or could not be clicked. Error: {e}")
