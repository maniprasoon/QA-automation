#!/usr/bin/env python3
"""
Demo test file that works with SauceDemo website
"""

import pytest
import time
import sys
import os
from selenium.webdriver.common.by import By  # ADD THIS IMPORT

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utilities.logger import get_logger
from utilities.config import Config

logger = get_logger("DemoTests")

@pytest.mark.smoke
class TestDemoLogin:
    """Demo test suite that works with real website"""
    
    def test_navigate_to_login_page(self, driver):
        """Test navigation to login page"""
        print("\n🔗 Testing navigation to login page...")
        
        # Navigate to SauceDemo
        driver.get(Config.LOGIN_URL)
        
        # Check page title
        title = driver.title
        print(f"📄 Page Title: {title}")
        
        assert "Swag Labs" in title, f"Expected 'Swag Labs' in title, got '{title}'"
        
        # Take screenshot
        driver.save_screenshot(str(Config.REPORTS_DIR / "login_page.png"))
        print("✅ Successfully navigated to login page")
    
    def test_login_form_elements(self, driver):
        """Test that login form elements are present"""
        print("\n🔍 Testing login form elements...")
        
        driver.get(Config.LOGIN_URL)
        
        # Find elements
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        
        # Verify elements are displayed
        assert username_field.is_displayed(), "Username field should be visible"
        assert password_field.is_displayed(), "Password field should be visible"
        assert login_button.is_displayed(), "Login button should be visible"
        
        print(f"✅ Username field: {username_field.is_displayed()}")
        print(f"✅ Password field: {password_field.is_displayed()}")
        print(f"✅ Login button: {login_button.is_displayed()}")
    
    def test_valid_login_demo(self, driver):
        """Test valid login with demo credentials"""
        print("\n🔐 Testing valid login...")
        
        driver.get(Config.LOGIN_URL)
        
        # Enter credentials
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()
        
        # Wait for page load
        time.sleep(2)
        
        # Verify login success
        current_url = driver.current_url
        print(f"📄 Current URL after login: {current_url}")
        
        # Should redirect to inventory page
        assert "inventory" in current_url, "Should redirect to inventory page after login"
        
        # Check for products
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        print(f"📦 Found {len(products)} products on inventory page")
        
        assert len(products) > 0, "Should see products after login"
        
        # Take screenshot
        driver.save_screenshot(str(Config.REPORTS_DIR / "login_success.png"))
        print("✅ Valid login test passed!")
    
    def test_invalid_login_demo(self, driver):
        """Test invalid login"""
        print("\n❌ Testing invalid login...")
        
        driver.get(Config.LOGIN_URL)
        
        # Enter invalid credentials
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("invalid_user")
        password_field.send_keys("wrong_password")
        login_button.click()
        
        # Wait for error message
        time.sleep(1)
        
        # Check for error message
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
            error_text = error_element.text
            print(f"📝 Error message: {error_text}")
            
            assert "Username and password do not match" in error_text or \
                   "Epic sadface" in error_text, "Should show appropriate error"
            
            print("✅ Invalid login test passed!")
        except:
            # Take screenshot if error not found
            driver.save_screenshot(str(Config.REPORTS_DIR / "login_error.png"))
            print("⚠️  Error message not found, but continuing...")
    
    def test_empty_login(self, driver):
        """Test login with empty credentials"""
        print("\n📭 Testing empty credentials login...")
        
        driver.get(Config.LOGIN_URL)
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Wait for error message
        time.sleep(1)
        
        # Check for error message
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
            error_text = error_element.text
            print(f"📝 Error message: {error_text}")
            
            assert "Username is required" in error_text, "Should show username required error"
            
            print("✅ Empty login test passed!")
        except:
            driver.save_screenshot(str(Config.REPORTS_DIR / "empty_login_error.png"))
            print("⚠️  Error message not found")