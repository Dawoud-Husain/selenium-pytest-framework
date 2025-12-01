from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class RegisterPage(BasePage):
    """Page object for the OpenCart registration page."""

    # Locators
    FIRST_NAME_INPUT = (By.ID, "input-firstname")
    LAST_NAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    NEWSLETTER_YES = (By.ID, "input-newsletter-yes")
    NEWSLETTER_NO = (By.ID, "input-newsletter-no")
    PRIVACY_POLICY_CHECKBOX = (By.CSS_SELECTOR, "input[name='agree']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, "#alert .alert-danger")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content h1")
    FIELD_ERRORS = (By.CSS_SELECTOR, ".invalid-feedback")
    LOGIN_LINK = (By.LINK_TEXT, "login page")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}?route=account/register"

    def open_register_page(self) -> "RegisterPage":
        """Navigate directly to the registration page."""
        self.open(self.url)
        self.wait_for_page_load()
        return self

    def enter_first_name(self, first_name: str) -> "RegisterPage":
        """Enter first name."""
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str) -> "RegisterPage":
        """Enter last name."""
        self.type_text(self.LAST_NAME_INPUT, last_name)
        return self

    def enter_email(self, email: str) -> "RegisterPage":
        """Enter email address."""
        self.type_text(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str) -> "RegisterPage":
        """Enter password."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def subscribe_to_newsletter(self, subscribe: bool = False) -> "RegisterPage":
        """Select newsletter subscription option."""
        if subscribe:
            self.click(self.NEWSLETTER_YES)
        else:
            self.click(self.NEWSLETTER_NO)
        return self

    def agree_to_privacy_policy(self) -> "RegisterPage":
        """Check the privacy policy agreement checkbox."""
        checkbox = self.find_element(self.PRIVACY_POLICY_CHECKBOX)
        if not checkbox.is_selected():
            self.click(self.PRIVACY_POLICY_CHECKBOX)
        return self

    def click_continue(self) -> None:
        """Click the continue/submit button."""
        self.click(self.CONTINUE_BUTTON)
        self.logger.info("Clicked continue button on registration form")

    def register(self, first_name: str, last_name: str, email: str,
                 password: str, newsletter: bool = False) -> None:
        """
        Complete the registration process.

        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            password: Account password
            newsletter: Subscribe to newsletter
        """
        self.logger.info(f"Registering new user: {email}")
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password(password)
        self.subscribe_to_newsletter(newsletter)
        self.agree_to_privacy_policy()
        self.click_continue()

    def is_registration_successful(self) -> bool:
        """Check if registration was successful."""
        try:
            success_text = self.get_text(self.SUCCESS_MESSAGE)
            return "Your Account Has Been Created" in success_text
        except:
            return False

    def is_error_displayed(self) -> bool:
        """Check if an error alert is displayed."""
        return self.is_element_visible(self.ERROR_ALERT, timeout=5)

    def get_error_message(self) -> str:
        """Get the error message text."""
        return self.get_text(self.ERROR_ALERT)

    def get_field_errors(self) -> list:
        """Get all field-level validation errors."""
        if self.is_element_present(self.FIELD_ERRORS):
            elements = self.find_elements(self.FIELD_ERRORS)
            return [el.text for el in elements if el.text]
        return []

    def is_on_register_page(self) -> bool:
        """Verify we are on the registration page."""
        return "account/register" in self.get_current_url()
