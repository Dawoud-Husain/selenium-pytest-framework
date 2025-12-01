import pytest
from pages import HomePage, LoginPage
from utilities.helpers import load_test_data


class TestLogin:
    """Test cases for login functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test."""
        self.driver = driver
        self.test_data = load_test_data("users.json")

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_loads(self, login_page: LoginPage):
        """Verify login page loads correctly."""
        assert login_page.is_on_login_page()
        assert "Login" in login_page.get_title() or "Account" in login_page.get_title()

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_elements_visible(self, login_page: LoginPage):
        """Verify all login page elements are visible."""
        assert login_page.is_element_visible(LoginPage.EMAIL_INPUT)
        assert login_page.is_element_visible(LoginPage.PASSWORD_INPUT)
        assert login_page.is_element_visible(LoginPage.LOGIN_BUTTON)
        assert login_page.is_element_visible(LoginPage.FORGOTTEN_PASSWORD_LINK)

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_empty_credentials(self, login_page: LoginPage):
        """Verify error message with empty credentials."""
        login_page.login("", "")
        assert login_page.is_error_displayed()

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_invalid_email(self, login_page: LoginPage):
        """Verify error message with invalid email format."""
        login_page.login("invalidemail", "password123")
        assert login_page.is_error_displayed()

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_wrong_password(self, login_page: LoginPage):
        """Verify error message with wrong password."""
        invalid_user = self.test_data["invalid_user"]
        login_page.login(invalid_user["email"], invalid_user["password"])
        assert login_page.is_error_displayed()
        error_msg = login_page.get_error_message()
        assert "Warning" in error_msg or "match" in error_msg.lower()

    @pytest.mark.smoke
    @pytest.mark.login
    def test_navigate_to_login_from_home(self, home_page: HomePage):
        """Verify navigation to login page from home page."""
        home_page.go_to_login()
        login_page = LoginPage(self.driver)
        assert login_page.is_on_login_page()

    @pytest.mark.regression
    @pytest.mark.login
    def test_forgotten_password_link(self, login_page: LoginPage):
        """Verify forgotten password link works."""
        login_page.click_forgotten_password()
        assert "forgotten" in login_page.get_current_url().lower()

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_empty_email(self, login_page: LoginPage):
        """Verify error when only password is provided."""
        login_page.login("", "password123")
        assert login_page.is_error_displayed()

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_empty_password(self, login_page: LoginPage):
        """Verify error when only email is provided."""
        login_page.login("test@example.com", "")
        assert login_page.is_error_displayed()
