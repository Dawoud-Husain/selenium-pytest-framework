from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class LoginPage(BasePage):
    """Page object for the OpenCart login page."""

    # Locators
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FORGOTTEN_PASSWORD_LINK = (By.LINK_TEXT, "Forgotten Password")
    REGISTER_LINK = (By.CSS_SELECTOR, "#content .col-sm-6:first-child a")
    ERROR_ALERT = (By.CSS_SELECTOR, "#alert .alert-danger")
    PAGE_TITLE = (By.CSS_SELECTOR, "#content h2")
    CONTINUE_BUTTON = (By.LINK_TEXT, "Continue")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}?route=account/login"

    def open_login_page(self) -> "LoginPage":
        """Navigate directly to the login page."""
        self.open(self.url)
        self.wait_for_page_load()
        return self

    def enter_email(self, email: str) -> "LoginPage":
        """Enter email address."""
        self.type_text(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Enter password."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
        self.logger.info("Clicked login button")

    def login(self, email: str, password: str) -> None:
        """
        Perform complete login action.

        Args:
            email: User email address
            password: User password
        """
        self.logger.info(f"Logging in with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def is_error_displayed(self) -> bool:
        """Check if an error message is displayed."""
        return self.is_element_visible(self.ERROR_ALERT, timeout=5)

    def get_error_message(self) -> str:
        """Get the error message text."""
        return self.get_text(self.ERROR_ALERT)

    def click_forgotten_password(self) -> None:
        """Click the forgotten password link."""
        self.click(self.FORGOTTEN_PASSWORD_LINK)

    def click_continue_to_register(self) -> None:
        """Click continue button to go to registration."""
        self.click(self.CONTINUE_BUTTON)

    def is_on_login_page(self) -> bool:
        """Verify we are on the login page."""
        return "account/login" in self.get_current_url()
