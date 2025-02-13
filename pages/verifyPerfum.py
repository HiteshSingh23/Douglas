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
    DROPDOWN_LOCATOR = (By.CLASS_NAME, "facet__title")  # The parent container of the dropdown
    DROPDOWN_OPTION_LOCATOR = (By.CLASS_NAME, "rc-scrollbars-view")  # Individual options inside the dropdown

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
            time.sleep(5)

            # Find all filter options in the dropdown
            options = self.browser.find_elements(*self.DROPDOWN_OPTION_LOCATOR)

            for option in options:
                option_text_element = option.find_element(By.XPATH, "//div[@class='facet-option__label']/div")
                option_text = option_text_element.text.strip()

                if option_text == filter_text.strip():
                    # Scroll the option into view
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", option_text_element)
                    time.sleep(1)  # Allow scrolling to complete

                    # Click the option
                    option_text_element.click()
                    time.sleep(12)  # Wait for the action to complete
                    break
                else:
                    print(f"Filter '{filter_text}' not found in the dropdown.")
