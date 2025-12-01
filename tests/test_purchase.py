import pytest
from pages import HomePage, FlightsPage, PurchasePage
from utilities.helpers import load_test_data


class TestPurchase:
    """Test cases for purchase functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver, home_page: HomePage, flights_page: FlightsPage):
        """Setup for each test."""
        self.driver = driver
        self.test_data = load_test_data("bookings.json")
        route = self.test_data["routes"]["paris_to_berlin"]
        home_page.search_flights(route["departure"], route["destination"])
        flights_page.select_flight(0)

    @pytest.mark.smoke
    @pytest.mark.purchase
    def test_purchase_page_loads(self, purchase_page: PurchasePage):
        """Verify purchase page loads correctly."""
        assert purchase_page.is_on_purchase_page()
        assert "purchase" in purchase_page.get_current_url().lower()

    @pytest.mark.smoke
    @pytest.mark.purchase
    def test_purchase_page_elements_visible(self, purchase_page: PurchasePage):
        """Verify all purchase page form elements are visible."""
        assert purchase_page.is_element_visible(PurchasePage.NAME_INPUT)
        assert purchase_page.is_element_visible(PurchasePage.ADDRESS_INPUT)
        assert purchase_page.is_element_visible(PurchasePage.CITY_INPUT)
        assert purchase_page.is_element_visible(PurchasePage.STATE_INPUT)
        assert purchase_page.is_element_visible(PurchasePage.ZIP_INPUT)
        assert purchase_page.is_element_visible(PurchasePage.CREDIT_CARD_INPUT)
        assert purchase_page.is_element_visible(PurchasePage.PURCHASE_BUTTON)

    @pytest.mark.regression
    @pytest.mark.purchase
    def test_fill_passenger_details(self, purchase_page: PurchasePage):
        """Verify filling passenger details works."""
        passenger = self.test_data["passenger"]
        purchase_page.fill_passenger_details(
            passenger["name"],
            passenger["address"],
            passenger["city"],
            passenger["state"],
            passenger["zip_code"]
        )
        assert purchase_page.get_attribute(PurchasePage.NAME_INPUT, "value") == passenger["name"]
        assert purchase_page.get_attribute(PurchasePage.CITY_INPUT, "value") == passenger["city"]

    @pytest.mark.regression
    @pytest.mark.purchase
    def test_fill_payment_details(self, purchase_page: PurchasePage):
        """Verify filling payment details works."""
        payment = self.test_data["payment"]
        purchase_page.fill_payment_details(
            payment["card_type"],
            payment["card_number"],
            payment["month"],
            payment["year"],
            payment["name_on_card"]
        )
        assert purchase_page.get_attribute(PurchasePage.CREDIT_CARD_INPUT, "value") == payment["card_number"]

    @pytest.mark.smoke
    @pytest.mark.purchase
    def test_complete_purchase_form(self, purchase_page: PurchasePage, confirmation_page):
        """Verify completing entire purchase form."""
        purchase_page.complete_purchase(
            self.test_data["passenger"],
            self.test_data["payment"]
        )
        assert confirmation_page.is_on_confirmation_page()
