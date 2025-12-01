from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FlightsPage(BasePage):
    """Page object for the BlazeDemo flights selection page."""

    # Locators
    FLIGHT_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    CHOOSE_FLIGHT_BUTTONS = (By.CSS_SELECTOR, "input[type='submit']")
    PAGE_HEADING = (By.CSS_SELECTOR, "h3")
    FLIGHT_PRICES = (By.CSS_SELECTOR, "table tbody tr td:nth-child(6)")
    AIRLINE_NAMES = (By.CSS_SELECTOR, "table tbody tr td:nth-child(3)")
    FLIGHT_NUMBERS = (By.CSS_SELECTOR, "table tbody tr td:nth-child(2)")

    def __init__(self, driver):
        super().__init__(driver)

    def is_on_flights_page(self) -> bool:
        """Check if we're on the flights page."""
        return "reserve" in self.get_current_url().lower()

    def get_page_heading(self) -> str:
        """Get the page heading text."""
        return self.get_text(self.PAGE_HEADING)

    def get_number_of_flights(self) -> int:
        """Get the number of available flights."""
        flights = self.find_elements(self.FLIGHT_ROWS)
        return len(flights)

    def select_flight(self, index: int = 0) -> None:
        """
        Select a flight by index.

        Args:
            index: Index of the flight to select (0-based)
        """
        self.logger.info(f"Selecting flight at index {index}")
        buttons = self.find_elements(self.CHOOSE_FLIGHT_BUTTONS)
        if index < len(buttons):
            buttons[index].click()
        else:
            raise IndexError(f"Flight index {index} out of range")

    def get_flight_prices(self) -> list:
        """Get all flight prices."""
        price_elements = self.find_elements(self.FLIGHT_PRICES)
        return [el.text for el in price_elements]

    def get_cheapest_flight_index(self) -> int:
        """Get the index of the cheapest flight."""
        prices = self.get_flight_prices()
        price_values = [float(p.replace('$', '')) for p in prices]
        return price_values.index(min(price_values))

    def select_cheapest_flight(self) -> None:
        """Select the cheapest available flight."""
        cheapest_index = self.get_cheapest_flight_index()
        self.select_flight(cheapest_index)
        self.logger.info(f"Selected cheapest flight at index {cheapest_index}")
