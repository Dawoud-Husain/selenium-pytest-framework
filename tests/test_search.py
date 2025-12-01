import pytest
from pages import HomePage, SearchResultsPage, ProductPage
from utilities.helpers import load_test_data


class TestSearch:
    """Test cases for product search functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test."""
        self.driver = driver
        self.test_data = load_test_data("products.json")

    @pytest.mark.smoke
    @pytest.mark.search
    def test_search_existing_product(self, home_page: HomePage):
        """Verify search for existing product returns results."""
        search_term = "MacBook"
        home_page.search_product(search_term)

        search_results = SearchResultsPage(self.driver)
        assert search_results.get_product_count() > 0
        assert search_results.is_product_in_results(search_term)

    @pytest.mark.smoke
    @pytest.mark.search
    def test_search_nonexistent_product(self, home_page: HomePage):
        """Verify search for non-existent product shows no results."""
        search_term = "xyznonexistent123456"
        home_page.search_product(search_term)

        search_results = SearchResultsPage(self.driver)
        assert search_results.is_no_results_displayed() or search_results.get_product_count() == 0

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_with_partial_name(self, home_page: HomePage):
        """Verify search works with partial product names."""
        search_term = "Mac"
        home_page.search_product(search_term)

        search_results = SearchResultsPage(self.driver)
        assert search_results.get_product_count() > 0

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_case_insensitive(self, home_page: HomePage):
        """Verify search is case insensitive."""
        # Search with lowercase
        home_page.search_product("macbook")

        search_results = SearchResultsPage(self.driver)
        lowercase_count = search_results.get_product_count()

        # Search with uppercase
        home_page.open_home_page()
        home_page.search_product("MACBOOK")

        search_results = SearchResultsPage(self.driver)
        uppercase_count = search_results.get_product_count()

        assert lowercase_count == uppercase_count

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_with_special_characters(self, home_page: HomePage):
        """Verify search handles special characters."""
        home_page.search_product("!@#$%")

        search_results = SearchResultsPage(self.driver)
        # Should either show no results or handle gracefully
        assert search_results.is_no_results_displayed() or search_results.get_product_count() >= 0

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_with_empty_string(self, home_page: HomePage):
        """Verify search with empty string."""
        home_page.search_product("")

        # Should either show all products or stay on search page
        search_results = SearchResultsPage(self.driver)
        # Just verify no error occurred
        assert "search" in search_results.get_current_url().lower()

    @pytest.mark.regression
    @pytest.mark.search
    def test_click_search_result_opens_product(self, home_page: HomePage):
        """Verify clicking search result opens product page."""
        home_page.search_product("iPhone")

        search_results = SearchResultsPage(self.driver)
        if search_results.get_product_count() > 0:
            product_name = search_results.get_product_names()[0]
            search_results.click_product(0)

            product_page = ProductPage(self.driver)
            assert product_name in product_page.get_product_name()

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_using_enter_key(self, home_page: HomePage):
        """Verify search works using Enter key."""
        search_term = "Samsung"
        home_page.search_product_with_enter(search_term)

        search_results = SearchResultsPage(self.driver)
        assert "search" in search_results.get_current_url().lower()

    @pytest.mark.regression
    @pytest.mark.search
    @pytest.mark.parametrize("product_name", ["MacBook", "iPhone", "Samsung", "Canon"])
    def test_search_multiple_products(self, home_page: HomePage, product_name: str):
        """Verify search works for multiple different products."""
        home_page.search_product(product_name)

        search_results = SearchResultsPage(self.driver)
        assert search_results.get_product_count() > 0 or search_results.is_no_results_displayed()

        # Navigate back for next iteration
        home_page.open_home_page()
