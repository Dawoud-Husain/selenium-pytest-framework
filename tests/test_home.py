import pytest
from pages import HomePage
from utilities.helpers import load_test_data


class TestHomePage:
    """Test cases for home page functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test."""
        self.driver = driver
        self.test_data = load_test_data("bookings.json")

    @pytest.mark.smoke
    def test_home_page_loads(self, home_page: HomePage):
        """Verify home page loads correctly."""
        assert "blazedemo" in home_page.get_current_url().lower()
        assert home_page.is_logo_displayed()

    @pytest.mark.smoke
    def test_home_page_elements_visible(self, home_page: HomePage):
        """Verify all home page elements are visible."""
        assert home_page.is_element_visible(HomePage.DEPARTURE_SELECT)
        assert home_page.is_element_visible(HomePage.DESTINATION_SELECT)
        assert home_page.is_element_visible(HomePage.FIND_FLIGHTS_BUTTON)

    @pytest.mark.smoke
    def test_search_flights(self, home_page: HomePage):
        """Verify searching for flights works."""
        route = self.test_data["routes"]["paris_to_berlin"]
        home_page.search_flights(route["departure"], route["destination"])
        assert "reserve" in home_page.get_current_url().lower()

    @pytest.mark.regression
    def test_select_departure_city(self, home_page: HomePage):
        """Verify selecting departure city works."""
        home_page.select_departure_city("Boston")
        selected_value = home_page.get_attribute(HomePage.DEPARTURE_SELECT, "value")
        assert selected_value == "Boston"

    @pytest.mark.regression
    def test_select_destination_city(self, home_page: HomePage):
        """Verify selecting destination city works."""
        home_page.select_destination_city("London")
        selected_value = home_page.get_attribute(HomePage.DESTINATION_SELECT, "value")
        assert selected_value == "London"

    @pytest.mark.regression
    def test_different_routes(self, home_page: HomePage):
        """Verify different route combinations work."""
        routes = self.test_data["routes"]
        for route_key, route in routes.items():
            home_page.open_home_page()
            home_page.search_flights(route["departure"], route["destination"])
            assert "reserve" in home_page.get_current_url().lower()
