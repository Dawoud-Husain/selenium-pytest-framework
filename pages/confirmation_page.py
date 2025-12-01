from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ConfirmationPage(BasePage):
    """Page object for the BlazeDemo confirmation page."""

    # Locators
    CONFIRMATION_HEADING = (By.CSS_SELECTOR, "h1")
    CONFIRMATION_MESSAGE = (By.CSS_SELECTOR, ".hero-unit p:first-of-type")
    TRANSACTION_ID = (By.CSS_SELECTOR, "tr:nth-child(1) td:nth-child(2)")
    STATUS = (By.CSS_SELECTOR, "tr:nth-child(2) td:nth-child(2)")
    AMOUNT = (By.CSS_SELECTOR, "tr:nth-child(3) td:nth-child(2)")
    CARD_NUMBER = (By.CSS_SELECTOR, "tr:nth-child(4) td:nth-child(2)")
    EXPIRATION = (By.CSS_SELECTOR, "tr:nth-child(5) td:nth-child(2)")
    AUTH_CODE = (By.CSS_SELECTOR, "tr:nth-child(6) td:nth-child(2)")
    TIMESTAMP = (By.CSS_SELECTOR, "tr:nth-child(7) td:nth-child(2)")
    ALL_DETAILS = (By.CSS_SELECTOR, "table tr")

    def __init__(self, driver):
        super().__init__(driver)

    def is_on_confirmation_page(self) -> bool:
        """Check if we're on the confirmation page."""
        return "confirmation" in self.get_current_url().lower()

    def get_confirmation_heading(self) -> str:
        """Get the confirmation heading text."""
        return self.get_text(self.CONFIRMATION_HEADING)

    def get_confirmation_message(self) -> str:
        """Get the confirmation message."""
        return self.get_text(self.CONFIRMATION_MESSAGE)

    def get_transaction_id(self) -> str:
        """Get the transaction ID."""
        return self.get_text(self.TRANSACTION_ID)

    def get_status(self) -> str:
        """Get the purchase status."""
        return self.get_text(self.STATUS)

    def get_amount(self) -> str:
        """Get the purchase amount."""
        return self.get_text(self.AMOUNT)

    def get_auth_code(self) -> str:
        """Get the authorization code."""
        return self.get_text(self.AUTH_CODE)

    def is_purchase_successful(self) -> bool:
        """Check if the purchase was successful."""
        heading = self.get_confirmation_heading().lower()
        return "thank you" in heading or "confirmation" in heading
