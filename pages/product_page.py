from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page object for the OpenCart product detail page."""

    # Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, "#content h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".price-new")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "#tab-description")
    QUANTITY_INPUT = (By.ID, "input-quantity")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    ADD_TO_WISHLIST = (By.CSS_SELECTOR, "button[formaction*='wishlist']")
    ADD_TO_COMPARE = (By.CSS_SELECTOR, "button[formaction*='compare']")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".image-additional img")
    MAIN_IMAGE = (By.CSS_SELECTOR, ".image-thumb img")
    REVIEWS_TAB = (By.CSS_SELECTOR, "a[href='#tab-review']")
    DESCRIPTION_TAB = (By.CSS_SELECTOR, "a[href='#tab-description']")
    SPECIFICATION_TAB = (By.CSS_SELECTOR, "a[href='#tab-specification']")
    BRAND_LINK = (By.CSS_SELECTOR, "#content ul.list-unstyled a")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    STOCK_STATUS = (By.CSS_SELECTOR, "#content ul.list-unstyled li:last-child")
    PRODUCT_CODE = (By.CSS_SELECTOR, "#content ul.list-unstyled li:first-child")
    RATING_STARS = (By.CSS_SELECTOR, ".rating .fa-stack")

    def get_product_name(self) -> str:
        """Get the product name."""
        return self.get_text(self.PRODUCT_NAME)

    def get_product_price(self) -> str:
        """Get the product price."""
        return self.get_text(self.PRODUCT_PRICE)

    def set_quantity(self, quantity: int) -> "ProductPage":
        """Set the product quantity."""
        self.type_text(self.QUANTITY_INPUT, str(quantity))
        return self

    def get_quantity(self) -> int:
        """Get the current quantity value."""
        return int(self.get_attribute(self.QUANTITY_INPUT, "value"))

    def add_to_cart(self) -> None:
        """Add the product to cart."""
        self.logger.info(f"Adding product to cart: {self.get_product_name()}")
        self.click(self.ADD_TO_CART_BUTTON)

    def add_to_cart_with_quantity(self, quantity: int) -> None:
        """Add the product to cart with specified quantity."""
        self.set_quantity(quantity)
        self.add_to_cart()

    def add_to_wishlist(self) -> None:
        """Add the product to wishlist."""
        self.click(self.ADD_TO_WISHLIST)

    def add_to_compare(self) -> None:
        """Add the product to compare list."""
        self.click(self.ADD_TO_COMPARE)

    def is_success_message_displayed(self) -> bool:
        """Check if success message is displayed."""
        return self.is_element_visible(self.SUCCESS_ALERT, timeout=5)

    def get_success_message(self) -> str:
        """Get the success message text."""
        return self.get_text(self.SUCCESS_ALERT)

    def switch_to_reviews_tab(self) -> None:
        """Switch to the reviews tab."""
        self.click(self.REVIEWS_TAB)

    def switch_to_description_tab(self) -> None:
        """Switch to the description tab."""
        self.click(self.DESCRIPTION_TAB)

    def switch_to_specification_tab(self) -> None:
        """Switch to the specification tab."""
        self.click(self.SPECIFICATION_TAB)

    def get_stock_status(self) -> str:
        """Get the product stock status."""
        return self.get_text(self.STOCK_STATUS)

    def is_in_stock(self) -> bool:
        """Check if the product is in stock."""
        status = self.get_stock_status().lower()
        return "in stock" in status

    def click_main_image(self) -> None:
        """Click the main product image to enlarge."""
        self.click(self.MAIN_IMAGE)
