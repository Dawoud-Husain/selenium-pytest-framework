from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Tuple
from config.config import Config
from utilities.logger import get_logger


class BasePage:
    """Base page class containing common methods for all page objects."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = get_logger(self.__class__.__name__)

    def open(self, url: str) -> None:
        """Navigate to the specified URL."""
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def get_title(self) -> str:
        """Get the current page title."""
        return self.driver.title

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.driver.current_url

    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """
        Find a single element on the page.

        Args:
            locator: Tuple of (By, value) e.g., (By.ID, "element_id")

        Returns:
            WebElement if found
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """
        Find multiple elements on the page.

        Args:
            locator: Tuple of (By, value)

        Returns:
            List of WebElements
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: Tuple[str, str]) -> None:
        """Wait for element to be clickable and click it."""
        self.logger.debug(f"Clicking element: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Args:
            locator: Element locator
            text: Text to type
            clear_first: Whether to clear the field first
        """
        self.logger.debug(f"Typing '{text}' into element: {locator}")
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str]) -> str:
        """Get the text content of an element."""
        return self.find_element(locator).text

    def is_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Check if an element is visible on the page."""
        try:
            wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if an element is present in the DOM."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_element_to_disappear(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Wait for an element to disappear from the page."""
        try:
            wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
            wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def select_dropdown_by_text(self, locator: Tuple[str, str], text: str) -> None:
        """Select a dropdown option by visible text."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def select_dropdown_by_value(self, locator: Tuple[str, str], value: str) -> None:
        """Select a dropdown option by value attribute."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)

    def hover(self, locator: Tuple[str, str]) -> None:
        """Hover over an element."""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """Scroll the element into view."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """Get an attribute value from an element."""
        return self.find_element(locator).get_attribute(attribute)

    def wait_for_page_load(self) -> None:
        """Wait for the page to fully load."""
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def accept_alert(self) -> None:
        """Accept a JavaScript alert."""
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self) -> None:
        """Dismiss a JavaScript alert."""
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()
