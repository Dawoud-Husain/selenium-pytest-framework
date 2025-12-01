from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List


class SearchResultsPage(BasePage):
    """Page object for the OpenCart search results page."""

    # Locators
    SEARCH_INPUT = (By.ID, "input-search")
    SEARCH_BUTTON = (By.ID, "button-search")
    SEARCH_IN_DESCRIPTION = (By.ID, "input-description")
    CATEGORY_DROPDOWN = (By.NAME, "category_id")
    SEARCH_SUBCATEGORIES = (By.NAME, "sub_category")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "#product-list .product-thumb")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "#product-list .product-thumb .description h4 a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "#product-list .product-thumb .price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "#product-list button[formaction*='cart.add']")
    ADD_TO_WISHLIST_BUTTONS = (By.CSS_SELECTOR, "#product-list button[formaction*='wishlist']")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "#content p")
    SORT_DROPDOWN = (By.ID, "input-sort")
    SHOW_DROPDOWN = (By.ID, "input-limit")
    LIST_VIEW_BUTTON = (By.ID, "button-list")
    GRID_VIEW_BUTTON = (By.ID, "button-grid")
    PAGINATION = (By.CSS_SELECTOR, ".pagination")
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb")
    COMPARE_BUTTONS = (By.CSS_SELECTOR, "#product-list button[formaction*='compare']")

    def get_product_count(self) -> int:
        """Get the number of products in search results."""
        products = self.driver.find_elements(*self.PRODUCT_ITEMS)
        return len(products)

    def get_product_names(self) -> List[str]:
        """Get names of all products in search results."""
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_product_prices(self) -> List[str]:
        """Get prices of all products in search results."""
        elements = self.find_elements(self.PRODUCT_PRICES)
        return [el.text for el in elements]

    def click_product(self, index: int = 0) -> None:
        """Click on a product by index to view details."""
        products = self.find_elements(self.PRODUCT_NAMES)
        if index < len(products):
            self.logger.info(f"Clicking product at index {index}: {products[index].text}")
            products[index].click()

    def click_product_by_name(self, name: str) -> bool:
        """
        Click on a product by name.

        Args:
            name: Product name (partial match)

        Returns:
            True if product was found and clicked
        """
        products = self.find_elements(self.PRODUCT_NAMES)
        for product in products:
            if name.lower() in product.text.lower():
                self.logger.info(f"Clicking product: {product.text}")
                product.click()
                return True
        return False

    def add_to_cart(self, index: int = 0) -> None:
        """Add a product to cart by index."""
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if index < len(buttons):
            buttons[index].click()
            self.logger.info(f"Added product at index {index} to cart")

    def is_no_results_displayed(self) -> bool:
        """Check if 'no results' message is displayed."""
        try:
            text = self.get_text(self.NO_RESULTS_MESSAGE)
            return "no product" in text.lower() or "does not match" in text.lower()
        except:
            return False

    def sort_by(self, option: str) -> None:
        """
        Sort products by the specified option.

        Args:
            option: Sort option text (e.g., "Price (Low > High)")
        """
        self.select_dropdown_by_text(self.SORT_DROPDOWN, option)

    def set_items_per_page(self, count: str) -> None:
        """Set the number of items to show per page."""
        self.select_dropdown_by_text(self.SHOW_DROPDOWN, count)

    def switch_to_list_view(self) -> None:
        """Switch to list view."""
        self.click(self.LIST_VIEW_BUTTON)

    def switch_to_grid_view(self) -> None:
        """Switch to grid view."""
        self.click(self.GRID_VIEW_BUTTON)

    def is_product_in_results(self, product_name: str) -> bool:
        """Check if a product appears in search results."""
        names = self.get_product_names()
        return any(product_name.lower() in name.lower() for name in names)

    def refine_search(self, keyword: str, search_in_description: bool = False) -> None:
        """
        Refine the search with a new keyword.

        Args:
            keyword: Search keyword
            search_in_description: Whether to search in product descriptions
        """
        self.type_text(self.SEARCH_INPUT, keyword)
        if search_in_description:
            checkbox = self.find_element(self.SEARCH_IN_DESCRIPTION)
            if not checkbox.is_selected():
                self.click(self.SEARCH_IN_DESCRIPTION)
        self.click(self.SEARCH_BUTTON)
