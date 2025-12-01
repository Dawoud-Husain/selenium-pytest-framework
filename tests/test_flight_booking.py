import pytest
from pages import HomePage, FlightsPage, PurchasePage, ConfirmationPage
from utilities.helpers import load_test_data


class TestFlightBooking:
    """Test cases for complete flight booking flow."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test."""
        self.driver = driver
        self.test_data = load_test_data("bookings.json")

    @pytest.mark.smoke
    @pytest.mark.booking
    def test_complete_booking_flow(self, home_page: HomePage, flights_page: FlightsPage,
                                   purchase_page: PurchasePage, confirmation_page: ConfirmationPage):
        """Verify complete flight booking process from search to confirmation."""
        route = self.test_data["routes"]["paris_to_berlin"]

        home_page.search_flights(route["departure"], route["destination"])

        assert flights_page.is_on_flights_page()
        assert flights_page.get_number_of_flights() > 0

        flights_page.select_flight(0)

        assert purchase_page.is_on_purchase_page()

        purchase_page.complete_purchase(
            self.test_data["passenger"],
            self.test_data["payment"]
        )

        assert confirmation_page.is_on_confirmation_page()
        assert confirmation_page.is_purchase_successful()

    @pytest.mark.smoke
    @pytest.mark.booking
    def test_booking_with_cheapest_flight(self, home_page: HomePage, flights_page: FlightsPage,
                                         purchase_page: PurchasePage, confirmation_page: ConfirmationPage):
        """Verify booking with the cheapest available flight."""
        route = self.test_data["routes"]["boston_to_london"]

        home_page.search_flights(route["departure"], route["destination"])

        flights_page.select_cheapest_flight()

        assert purchase_page.is_on_purchase_page()

        purchase_page.complete_purchase(
            self.test_data["passenger"],
            self.test_data["payment"]
        )

        assert confirmation_page.is_on_confirmation_page()
        assert confirmation_page.get_transaction_id()

    @pytest.mark.regression
    @pytest.mark.booking
    def test_confirmation_details(self, home_page: HomePage, flights_page: FlightsPage,
                                  purchase_page: PurchasePage, confirmation_page: ConfirmationPage):
        """Verify all confirmation details are displayed."""
        route = self.test_data["routes"]["portland_to_dublin"]

        home_page.search_flights(route["departure"], route["destination"])
        flights_page.select_flight(0)
        purchase_page.complete_purchase(
            self.test_data["passenger"],
            self.test_data["payment"]
        )

        assert confirmation_page.get_transaction_id()
        assert confirmation_page.get_status()
        assert confirmation_page.get_amount()
        assert confirmation_page.get_auth_code()
