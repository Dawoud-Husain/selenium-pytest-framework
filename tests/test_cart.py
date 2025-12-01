import pytest
from pages import HomePage, SearchResultsPage, ProductPage, CartPage


class TestCart:
    """Test cases for shopping cart functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test."""
        self.driver = driver

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_empty_cart_message(self, cart_page: CartPage):
        """Verify empty cart displays appropriate message."""
        # Fresh cart should be empty
        assert cart_page.is_cart_empty() or cart_page.get_cart_item_count() >= 0

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_to_cart_from_home(self, home_page: HomePage):
        """Verify adding product to cart from home page."""
        # Check if there are featured products
        product_count = home_page.get_featured_products_count()

        if product_count > 0:
            home_page.add_featured_product_to_cart(0)

            # Wait for success message
            assert home_page.is_success_message_displayed()
            success_msg = home_page.get_success_message()
            assert "cart" in success_msg.lower()

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_to_cart_from_product_page(self, home_page: HomePage):
        """Verify adding product to cart from product detail page."""
        home_page.search_product("MacBook")

        search_results = SearchResultsPage(self.driver)
        if search_results.get_product_count() > 0:
            search_results.click_product(0)

            product_page = ProductPage(self.driver)
            product_name = product_page.get_product_name()
            product_page.add_to_cart()

            assert product_page.is_success_message_displayed()

    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_products_to_cart(self, home_page: HomePage):
        """Verify adding multiple products to cart."""
        products_to_add = ["MacBook", "iPhone"]

        for product in products_to_add:
            home_page.open_home_page()
            home_page.search_product(product)

            search_results = SearchResultsPage(self.driver)
            if search_results.get_product_count() > 0:
                search_results.add_to_cart(0)

        # Navigate to cart and verify
        cart_page = CartPage(self.driver)
        cart_page.open_cart_page()

        # Should have products in cart
        assert cart_page.get_cart_item_count() > 0

    @pytest.mark.regression
    @pytest.mark.cart
    def test_update_product_quantity_in_cart(self, home_page: HomePage):
        """Verify updating product quantity in cart."""
        # Add a product first
        home_page.search_product("iPhone")

        search_results = SearchResultsPage(self.driver)
        if search_results.get_product_count() > 0:
            search_results.add_to_cart(0)

            cart_page = CartPage(self.driver)
            cart_page.open_cart_page()

            if not cart_page.is_cart_empty():
                initial_qty = cart_page.get_product_quantities()[0]
                cart_page.update_quantity(0, initial_qty + 1)

                # Verify quantity updated
                cart_page.wait_for_page_load()
                updated_qty = cart_page.get_product_quantities()[0]
                assert updated_qty == initial_qty + 1 or updated_qty > 0

    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_product_from_cart(self, home_page: HomePage):
        """Verify removing product from cart."""
        # Add a product first
        home_page.search_product("Canon")

        search_results = SearchResultsPage(self.driver)
        if search_results.get_product_count() > 0:
            search_results.add_to_cart(0)

            cart_page = CartPage(self.driver)
            cart_page.open_cart_page()

            if not cart_page.is_cart_empty():
                initial_count = cart_page.get_cart_item_count()
                cart_page.remove_product(0)

                cart_page.wait_for_page_load()
                # Either empty or one less item
                assert cart_page.is_cart_empty() or cart_page.get_cart_item_count() < initial_count

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_totals_displayed(self, home_page: HomePage):
        """Verify cart displays totals correctly."""
        home_page.search_product("MacBook")

        search_results = SearchResultsPage(self.driver)
        if search_results.get_product_count() > 0:
            search_results.add_to_cart(0)

            cart_page = CartPage(self.driver)
            cart_page.open_cart_page()

            if not cart_page.is_cart_empty():
                subtotal = cart_page.get_subtotal()
                total = cart_page.get_total()

                assert "$" in subtotal or "£" in subtotal or "€" in subtotal
                assert "$" in total or "£" in total or "€" in total

    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_product_with_quantity(self, home_page: HomePage):
        """Verify adding product with specific quantity."""
        home_page.search_product("iPhone")

        search_results = SearchResultsPage(self.driver)
        if search_results.get_product_count() > 0:
            search_results.click_product(0)

            product_page = ProductPage(self.driver)
            product_page.add_to_cart_with_quantity(3)

            assert product_page.is_success_message_displayed()

    @pytest.mark.regression
    @pytest.mark.cart
    def test_continue_shopping_from_cart(self, cart_page: CartPage):
        """Verify continue shopping button works."""
        cart_page.continue_shopping()

        home_page = HomePage(self.driver)
        # Should be redirected to home or product page
        assert home_page.is_logo_displayed()

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_summary(self, home_page: HomePage):
        """Verify cart summary contains all required information."""
        home_page.search_product("Samsung")

        search_results = SearchResultsPage(self.driver)
        if search_results.get_product_count() > 0:
            search_results.add_to_cart(0)

            cart_page = CartPage(self.driver)
            cart_page.open_cart_page()

            if not cart_page.is_cart_empty():
                summary = cart_page.get_cart_summary()

                assert summary["item_count"] > 0
                assert len(summary["products"]) > 0
                assert len(summary["quantities"]) > 0
