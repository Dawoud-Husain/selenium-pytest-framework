from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from config.config import Config


class HomePage(BasePage):
    """Page object for the OpenCart home page."""

    # Locators
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    CART_BUTTON = (By.ID, "header-cart")
    CART_TOTAL = (By.CSS_SELECTOR, "#header-cart button")
    MY_ACCOUNT_DROPDOWN = (By.CSS_SELECTOR, ".nav .dropdown:nth-child(2) > a")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    MY_ACCOUNT_LINK = (By.LINK_TEXT, "My Account")
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, "#content .product-thumb")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "#content .product-thumb .description h4 a")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "#content .product-thumb button[title='Add to Cart']")
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, ".btn-group .dropdown-toggle")
    CURRENCY_OPTIONS = (By.CSS_SELECTOR, ".btn-group .dropdown-menu button")
    NAVBAR_CATEGORIES = (By.CSS_SELECTOR, "#narbar-menu .nav-item")
    SLIDESHOW = (By.CSS_SELECTOR, "#carousel-banner-0")
    LOGO = (By.CSS_SELECTOR, "#logo img")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = Config.BASE_URL

    def open_home_page(self) -> "HomePage":
        """Navigate to the home page."""
        self.open(self.url)
        self.wait_for_page_load()
        self.logger.info("Opened OpenCart home page")
        return self

    def search_product(self, product_name: str) -> None:
        """
        Search for a product using the search bar.

        Args:
            product_name: Name of the product to search for
        """
        self.logger.info(f"Searching for product: {product_name}")
        self.type_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)

    def search_product_with_enter(self, product_name: str) -> None:
        """Search for a product by pressing Enter."""
        self.type_text(self.SEARCH_INPUT, product_name)
        self.find_element(self.SEARCH_INPUT).send_keys(Keys.ENTER)

    def click_my_account(self) -> None:
        """Click the My Account dropdown."""
        self.click(self.MY_ACCOUNT_DROPDOWN)

    def go_to_login(self) -> None:
        """Navigate to the login page."""
        self.logger.info("Navigating to login page")
        self.click_my_account()
        self.click(self.LOGIN_LINK)

    def go_to_register(self) -> None:
        """Navigate to the registration page."""
        self.logger.info("Navigating to registration page")
        self.click_my_account()
        self.click(self.REGISTER_LINK)

    def logout(self) -> None:
        """Logout the current user."""
        self.logger.info("Logging out")
        self.click_my_account()
        self.click(self.LOGOUT_LINK)

    def is_user_logged_in(self) -> bool:
        """Check if a user is logged in by looking for logout link."""
        self.click_my_account()
        return self.is_element_visible(self.LOGOUT_LINK, timeout=3)

    def get_featured_products_count(self) -> int:
        """Get the number of featured products on the home page."""
        products = self.find_elements(self.FEATURED_PRODUCTS)
        return len(products)

    def get_featured_product_names(self) -> list:
        """Get names of all featured products."""
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def click_featured_product(self, index: int = 0) -> None:
        """Click on a featured product by index."""
        products = self.find_elements(self.PRODUCT_NAMES)
        if index < len(products):
            products[index].click()

    def add_featured_product_to_cart(self, index: int = 0) -> None:
        """Add a featured product to cart by index."""
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if index < len(add_buttons):
            add_buttons[index].click()
            self.logger.info(f"Added featured product {index} to cart")

    def is_success_message_displayed(self) -> bool:
        """Check if a success alert is displayed."""
        return self.is_element_visible(self.SUCCESS_ALERT, timeout=5)

    def get_success_message(self) -> str:
        """Get the success message text."""
        return self.get_text(self.SUCCESS_ALERT)

    def is_logo_displayed(self) -> bool:
        """Check if the logo is displayed."""
        return self.is_element_visible(self.LOGO)

    def is_slideshow_displayed(self) -> bool:
        """Check if the slideshow/carousel is displayed."""
        return self.is_element_visible(self.SLIDESHOW)
