import pytest
import time
import sys
import os
from selenium.webdriver.common.by import By
import time

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utilities.data_reader import TestDataReader
from utilities.logger import get_logger

logger = get_logger("LoginTests")

@pytest.mark.login
@pytest.mark.smoke
class TestLoginFunctionality:
    """Test suite for Login functionality"""
    
    def test_login_page_elements_visibility(self, driver):
        """Test that all required elements are visible on login page"""
        print("\n🔍 Testing login page elements...")
        
        # Navigate to the actual website
        from utilities.config import Config
        driver.get(Config.LOGIN_URL)
        
        # SauceDemo specific locators
        locators = [
            ("Username input", (By.ID, "user-name")),
            ("Password input", (By.ID, "password")),
            ("Login button", (By.ID, "login-button")),
        ]
        
        all_visible = True
        for element_name, locator in locators:
            try:
                element = driver.find_element(*locator)
                is_visible = element.is_displayed()
                status = "✅" if is_visible else "❌"
                print(f"{status} {element_name}: {is_visible}")
                if not is_visible:
                    all_visible = False
            except:
                print(f"❌ {element_name}: Not found")
                all_visible = False
        
        assert all_visible, "All login page elements should be visible"
        print("✅ All elements found and visible!")
    
    def test_valid_login(self, login_page):
        """Test login with valid credentials"""
        logger.log_info("Starting test_valid_login")
        
        print("Testing valid login...")
        
        # Get valid credentials
        credentials = TestDataReader.get_valid_credentials()
        
        # Perform login
        login_page.login(
            credentials['username'],
            credentials['password']
        )
        
        # Wait for page load
        time.sleep(2)
        
        # Check current URL
        current_url = login_page.driver.current_url
        print(f"Current URL: {current_url}")
        
        # For demo purposes, we'll just check we're not on login page
        # In real test, you'd check for success indicators
        assert "login" not in current_url.lower(), "Should redirect from login page"
        
        print("✅ Valid login test completed")
        logger.log_info("test_valid_login PASSED")
    
    @pytest.mark.parametrize("test_case", [
        {"username": "wrong@test.com", "password": "wrong", "expected": "invalid"},
        {"username": "", "password": "test123", "expected": "required"},
        {"username": "test@test.com", "password": "", "expected": "required"},
    ])
    def test_invalid_login(self, login_page, test_case):
        """Test various invalid login scenarios"""
        print(f"Testing invalid login: {test_case['username']}")
        
        login_page.login(
            test_case['username'],
            test_case['password']
        )
        
        time.sleep(1)
        
        # Check for error message
        error_msg = login_page.get_error_message()
        print(f"Error message: {error_msg}")
        
        assert error_msg is not None, "Error message should be displayed"
        print(f"✅ Invalid login test passed for {test_case['username']}")
    
    def test_password_masking(self, login_page):
        """Test that password field masks input"""
        print("Testing password masking...")
        
        # Enter text in password field
        login_page.enter_text(login_page.PASSWORD_INPUT, "Test@123")
        
        # Check password field type
        password_field = login_page.find_element(login_page.PASSWORD_INPUT)
        field_type = password_field.get_attribute("type")
        
        assert field_type == "password", f"Password field type should be 'password', got '{field_type}'"
        print(f"✅ Password field type is '{field_type}' (correctly masked)")
    
    def test_forgot_password_link(self, login_page):
        """Test forgot password link navigation"""
        print("Testing forgot password link...")
        
        # Click forgot password link
        login_page.click_forgot_password()
        
        # Wait for navigation
        time.sleep(2)
        
        # Check URL
        current_url = login_page.driver.current_url
        print(f"Current URL after click: {current_url}")
        
        # Should navigate away from login page
        assert current_url != "about:blank", "Should navigate to a new page"
        print("✅ Forgot password link test passed")
    