from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class HomePage(BasePage):
    """Page object for the BlazeDemo home page."""

    # Locators
    DEPARTURE_SELECT = (By.NAME, "fromPort")
    DESTINATION_SELECT = (By.NAME, "toPort")
    FIND_FLIGHTS_BUTTON = (By.CSS_SELECTOR, "input[type='submit']")
    TITLE_HEADING = (By.CSS_SELECTOR, "h1")
    LOGO = (By.CSS_SELECTOR, ".navbar-brand")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = Config.BASE_URL

    def open_home_page(self) -> "HomePage":
        """Navigate to the home page."""
        self.open(self.url)
        self.wait_for_page_load()
        self.logger.info("Opened BlazeDemo home page")
        return self

    def select_departure_city(self, city: str) -> None:
        """
        Select departure city from dropdown.

        Args:
            city: Name of the departure city
        """
        self.logger.info(f"Selecting departure city: {city}")
        self.select_dropdown_by_value(self.DEPARTURE_SELECT, city)

    def select_destination_city(self, city: str) -> None:
        """
        Select destination city from dropdown.

        Args:
            city: Name of the destination city
        """
        self.logger.info(f"Selecting destination city: {city}")
        self.select_dropdown_by_value(self.DESTINATION_SELECT, city)

    def click_find_flights(self) -> None:
        """Click the Find Flights button."""
        self.logger.info("Clicking Find Flights button")
        self.click(self.FIND_FLIGHTS_BUTTON)

    def search_flights(self, departure: str, destination: str) -> None:
        """
        Complete search for flights.

        Args:
            departure: Departure city
            destination: Destination city
        """
        self.select_departure_city(departure)
        self.select_destination_city(destination)
        self.click_find_flights()

    def get_page_heading(self) -> str:
        """Get the main heading text."""
        return self.get_text(self.TITLE_HEADING)

    def is_logo_displayed(self) -> bool:
        """Check if the logo is displayed."""
        return self.is_element_visible(self.LOGO)
