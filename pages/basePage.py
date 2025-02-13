from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def wait_for_element(self, locator: tuple, timeout=20) -> WebElement:
        """Wait for an element to be present."""
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple):
        """Wait for an element and click it."""
        element = self.wait_for_element(locator)
        element.click()

    def find_shadow_element(self, shadow_host_locator: tuple, element_selector: str) -> WebElement:
        """Find an element inside a shadow DOM."""
        shadow_host = self.wait_for_element(shadow_host_locator)
        shadow_root = self.browser.execute_script("return arguments[0].shadowRoot", shadow_host)
        return shadow_root.find_element(By.CSS_SELECTOR, element_selector)
