import pytest
from pages import HomePage, FlightsPage
from utilities.helpers import load_test_data


class TestFlights:
    """Test cases for flight selection functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver, home_page: HomePage):
        """Setup for each test."""
        self.driver = driver
        self.test_data = load_test_data("bookings.json")
        route = self.test_data["routes"]["paris_to_berlin"]
        home_page.search_flights(route["departure"], route["destination"])

    @pytest.mark.smoke
    @pytest.mark.flights
    def test_flights_page_loads(self, flights_page: FlightsPage):
        """Verify flights page loads correctly."""
        assert flights_page.is_on_flights_page()
        assert "reserve" in flights_page.get_current_url().lower()

    @pytest.mark.smoke
    @pytest.mark.flights
    def test_flights_displayed(self, flights_page: FlightsPage):
        """Verify flights are displayed on the page."""
        number_of_flights = flights_page.get_number_of_flights()
        assert number_of_flights > 0
        assert number_of_flights >= 3

    @pytest.mark.regression
    @pytest.mark.flights
    def test_flight_prices_displayed(self, flights_page: FlightsPage):
        """Verify all flights have prices displayed."""
        prices = flights_page.get_flight_prices()
        assert len(prices) > 0
        for price in prices:
            assert "$" in price

    @pytest.mark.regression
    @pytest.mark.flights
    def test_select_specific_flight(self, flights_page: FlightsPage, purchase_page):
        """Verify selecting a specific flight navigates to purchase page."""
        flights_page.select_flight(1)
        assert purchase_page.is_on_purchase_page()

    @pytest.mark.regression
    @pytest.mark.flights
    def test_cheapest_flight_selection(self, flights_page: FlightsPage):
        """Verify cheapest flight can be identified."""
        cheapest_index = flights_page.get_cheapest_flight_index()
        assert cheapest_index >= 0
        prices = flights_page.get_flight_prices()
        assert cheapest_index < len(prices)
