from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List, Dict


class CartPage(BasePage):
    """Page object for the OpenCart shopping cart page."""

    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, "#shopping-cart tbody tr")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "#shopping-cart tbody tr td:nth-child(2) a")
    PRODUCT_QUANTITIES = (By.CSS_SELECTOR, "#shopping-cart input[name*='quantity']")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "#shopping-cart tbody tr td:nth-child(5)")
    PRODUCT_TOTALS = (By.CSS_SELECTOR, "#shopping-cart tbody tr td:nth-child(6)")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "#shopping-cart button[type='submit'].btn-danger")
    UPDATE_BUTTONS = (By.CSS_SELECTOR, "#shopping-cart button[type='submit'].btn-primary")
    SUBTOTAL = (By.CSS_SELECTOR, "#checkout-total tr:first-child td:last-child")
    TOTAL = (By.CSS_SELECTOR, "#checkout-total tr:last-child td:last-child")
    CHECKOUT_BUTTON = (By.LINK_TEXT, "Checkout")
    CONTINUE_SHOPPING = (By.LINK_TEXT, "Continue Shopping")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "#content p")
    COUPON_INPUT = (By.ID, "input-coupon")
    APPLY_COUPON = (By.ID, "button-coupon")
    ESTIMATE_SHIPPING = (By.CSS_SELECTOR, "#accordion .accordion-button")

    def __init__(self, driver):
        super().__init__(driver)
        from config.config import Config
        self.url = f"{Config.BASE_URL}?route=checkout/cart"

    def open_cart_page(self) -> "CartPage":
        """Navigate directly to the cart page."""
        self.open(self.url)
        self.wait_for_page_load()
        return self

    def get_cart_item_count(self) -> int:
        """Get the number of items in the cart."""
        try:
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(items)
        except:
            return 0

    def is_cart_empty(self) -> bool:
        """Check if the cart is empty."""
        try:
            message = self.get_text(self.EMPTY_CART_MESSAGE)
            return "empty" in message.lower() or "no products" in message.lower()
        except:
            return self.get_cart_item_count() == 0

    def get_product_names(self) -> List[str]:
        """Get names of all products in cart."""
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_product_quantities(self) -> List[int]:
        """Get quantities of all products in cart."""
        elements = self.find_elements(self.PRODUCT_QUANTITIES)
        return [int(el.get_attribute("value")) for el in elements]

    def update_quantity(self, index: int, quantity: int) -> None:
        """
        Update quantity for a product by index.

        Args:
            index: Product index (0-based)
            quantity: New quantity
        """
        quantity_inputs = self.find_elements(self.PRODUCT_QUANTITIES)
        update_buttons = self.find_elements(self.UPDATE_BUTTONS)

        if index < len(quantity_inputs):
            quantity_inputs[index].clear()
            quantity_inputs[index].send_keys(str(quantity))
            update_buttons[index].click()
            self.logger.info(f"Updated product {index} quantity to {quantity}")

    def remove_product(self, index: int = 0) -> None:
        """Remove a product from cart by index."""
        remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
        if index < len(remove_buttons):
            self.logger.info(f"Removing product at index {index}")
            remove_buttons[index].click()

    def remove_all_products(self) -> None:
        """Remove all products from the cart."""
        while not self.is_cart_empty():
            self.remove_product(0)
            self.wait_for_page_load()

    def get_subtotal(self) -> str:
        """Get the cart subtotal."""
        return self.get_text(self.SUBTOTAL)

    def get_total(self) -> str:
        """Get the cart total."""
        return self.get_text(self.TOTAL)

    def proceed_to_checkout(self) -> None:
        """Click the checkout button."""
        self.logger.info("Proceeding to checkout")
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        """Click continue shopping button."""
        self.click(self.CONTINUE_SHOPPING)

    def apply_coupon(self, coupon_code: str) -> None:
        """
        Apply a coupon code.

        Args:
            coupon_code: The coupon code to apply
        """
        self.type_text(self.COUPON_INPUT, coupon_code)
        self.click(self.APPLY_COUPON)

    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if a product is in the cart."""
        names = self.get_product_names()
        return any(product_name.lower() in name.lower() for name in names)

    def get_cart_summary(self) -> Dict:
        """Get a summary of the cart contents."""
        return {
            "item_count": self.get_cart_item_count(),
            "products": self.get_product_names(),
            "quantities": self.get_product_quantities(),
            "subtotal": self.get_subtotal() if not self.is_cart_empty() else "$0.00",
            "total": self.get_total() if not self.is_cart_empty() else "$0.00"
        }
