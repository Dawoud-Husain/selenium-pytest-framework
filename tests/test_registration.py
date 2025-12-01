import pytest
from pages import HomePage, RegisterPage
from utilities.helpers import generate_random_user


class TestRegistration:
    """Test cases for user registration functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test."""
        self.driver = driver

    @pytest.mark.smoke
    @pytest.mark.registration
    def test_register_page_loads(self, register_page: RegisterPage):
        """Verify registration page loads correctly."""
        assert register_page.is_on_register_page()

    @pytest.mark.smoke
    @pytest.mark.registration
    def test_register_page_elements_visible(self, register_page: RegisterPage):
        """Verify all registration form elements are visible."""
        assert register_page.is_element_visible(RegisterPage.FIRST_NAME_INPUT)
        assert register_page.is_element_visible(RegisterPage.LAST_NAME_INPUT)
        assert register_page.is_element_visible(RegisterPage.EMAIL_INPUT)
        assert register_page.is_element_visible(RegisterPage.PASSWORD_INPUT)
        assert register_page.is_element_visible(RegisterPage.CONTINUE_BUTTON)

    @pytest.mark.smoke
    @pytest.mark.registration
    def test_successful_registration(self, register_page: RegisterPage):
        """Verify successful user registration with valid data."""
        user = generate_random_user()

        register_page.register(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            password=user["password"],
            newsletter=False
        )

        # Check for success - either success message or redirect to account page
        current_url = register_page.get_current_url()
        assert register_page.is_registration_successful() or "account/success" in current_url

    @pytest.mark.regression
    @pytest.mark.registration
    def test_registration_with_empty_fields(self, register_page: RegisterPage):
        """Verify validation errors with empty fields."""
        register_page.agree_to_privacy_policy()
        register_page.click_continue()

        # Should show field validation errors or stay on page
        assert register_page.is_on_register_page()

    @pytest.mark.regression
    @pytest.mark.registration
    def test_registration_without_privacy_policy(self, register_page: RegisterPage):
        """Verify error when privacy policy is not accepted."""
        user = generate_random_user()

        register_page.enter_first_name(user["first_name"])
        register_page.enter_last_name(user["last_name"])
        register_page.enter_email(user["email"])
        register_page.enter_password(user["password"])
        # Don't agree to privacy policy
        register_page.click_continue()

        # Should show error or stay on registration page
        assert register_page.is_on_register_page() or register_page.is_error_displayed()

    @pytest.mark.regression
    @pytest.mark.registration
    def test_registration_with_invalid_email(self, register_page: RegisterPage):
        """Verify validation for invalid email format."""
        register_page.register(
            first_name="Test",
            last_name="User",
            email="invalidemail",
            password="password123"
        )

        # Should show error or stay on page
        assert register_page.is_on_register_page()

    @pytest.mark.regression
    @pytest.mark.registration
    def test_registration_with_short_password(self, register_page: RegisterPage):
        """Verify validation for password length."""
        user = generate_random_user()

        register_page.register(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            password="123"  # Too short
        )

        # Should show error about password length
        assert register_page.is_on_register_page()

    @pytest.mark.regression
    @pytest.mark.registration
    def test_navigate_to_register_from_home(self, home_page: HomePage):
        """Verify navigation to registration from home page."""
        home_page.go_to_register()
        register_page = RegisterPage(self.driver)
        assert register_page.is_on_register_page()

    @pytest.mark.regression
    @pytest.mark.registration
    def test_registration_with_newsletter_subscription(self, register_page: RegisterPage):
        """Verify registration with newsletter subscription."""
        user = generate_random_user()

        register_page.register(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            password=user["password"],
            newsletter=True  # Subscribe to newsletter
        )

        current_url = register_page.get_current_url()
        assert register_page.is_registration_successful() or "account/success" in current_url
