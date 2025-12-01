from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PurchasePage(BasePage):
    """Page object for the BlazeDemo purchase page."""

    # Locators
    NAME_INPUT = (By.ID, "inputName")
    ADDRESS_INPUT = (By.ID, "address")
    CITY_INPUT = (By.ID, "city")
    STATE_INPUT = (By.ID, "state")
    ZIP_INPUT = (By.ID, "zipCode")
    CARD_TYPE_SELECT = (By.ID, "cardType")
    CREDIT_CARD_INPUT = (By.ID, "creditCardNumber")
    CREDIT_CARD_MONTH_INPUT = (By.ID, "creditCardMonth")
    CREDIT_CARD_YEAR_INPUT = (By.ID, "creditCardYear")
    NAME_ON_CARD_INPUT = (By.ID, "nameOnCard")
    PURCHASE_BUTTON = (By.CSS_SELECTOR, "input[type='submit']")
    PAGE_HEADING = (By.CSS_SELECTOR, "h2")
    AIRLINE_INFO = (By.CSS_SELECTOR, "p:nth-of-type(1)")
    FLIGHT_INFO = (By.CSS_SELECTOR, "p:nth-of-type(2)")
    PRICE_INFO = (By.CSS_SELECTOR, "p:nth-of-type(3)")

    def __init__(self, driver):
        super().__init__(driver)

    def is_on_purchase_page(self) -> bool:
        """Check if we're on the purchase page."""
        return "purchase" in self.get_current_url().lower()

    def get_page_heading(self) -> str:
        """Get the page heading text."""
        return self.get_text(self.PAGE_HEADING)

    def fill_passenger_details(self, name: str, address: str, city: str,
                               state: str, zip_code: str) -> None:
        """
        Fill in passenger details.

        Args:
            name: Passenger name
            address: Street address
            city: City
            state: State
            zip_code: ZIP code
        """
        self.logger.info(f"Filling passenger details for {name}")
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.ADDRESS_INPUT, address)
        self.type_text(self.CITY_INPUT, city)
        self.type_text(self.STATE_INPUT, state)
        self.type_text(self.ZIP_INPUT, zip_code)

    def fill_payment_details(self, card_type: str, card_number: str,
                            month: str, year: str, name_on_card: str) -> None:
        """
        Fill in payment details.

        Args:
            card_type: Type of credit card
            card_number: Credit card number
            month: Expiry month
            year: Expiry year
            name_on_card: Name on card
        """
        self.logger.info("Filling payment details")
        self.select_dropdown_by_value(self.CARD_TYPE_SELECT, card_type)
        self.type_text(self.CREDIT_CARD_INPUT, card_number)
        self.type_text(self.CREDIT_CARD_MONTH_INPUT, month)
        self.type_text(self.CREDIT_CARD_YEAR_INPUT, year)
        self.type_text(self.NAME_ON_CARD_INPUT, name_on_card)

    def complete_purchase(self, passenger_data: dict, payment_data: dict) -> None:
        """
        Complete the entire purchase form.

        Args:
            passenger_data: Dict with keys: name, address, city, state, zip_code
            payment_data: Dict with keys: card_type, card_number, month, year, name_on_card
        """
        self.fill_passenger_details(
            passenger_data['name'],
            passenger_data['address'],
            passenger_data['city'],
            passenger_data['state'],
            passenger_data['zip_code']
        )
        self.fill_payment_details(
            payment_data['card_type'],
            payment_data['card_number'],
            payment_data['month'],
            payment_data['year'],
            payment_data['name_on_card']
        )
        self.click_purchase()

    def click_purchase(self) -> None:
        """Click the Purchase Flight button."""
        self.logger.info("Clicking Purchase Flight button")
        self.click(self.PURCHASE_BUTTON)

    def get_total_price(self) -> str:
        """Get the total price displayed."""
        price_text = self.get_text(self.PRICE_INFO)
        return price_text
