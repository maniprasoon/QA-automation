from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.config import Config

class LoginPage(BasePage):
    """Page Object for Login Page - Updated for SauceDemo"""
    
    # Locators for SauceDemo website
    USERNAME_INPUT = (By.ID, "user-name")  # Changed from "username"
    PASSWORD_INPUT = (By.ID, "password")   # Same
    LOGIN_BUTTON = (By.ID, "login-button") # Changed from "loginBtn"
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")  # SauceDemo error
    LOGIN_CONTAINER = (By.ID, "login_button_container")  # For validation
    
    # Note: SauceDemo doesn't have Forgot Password link
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(Config.LOGIN_URL)
        self.logger.log_info(f"Navigated to: {Config.LOGIN_URL}")
        self.logger.log_test_start()
    
    def login(self, username, password):
        """Perform login with given credentials"""
        self.logger.log_info(f"Attempting login with username: {username}")
        
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        
        self.logger.log_info("Login button clicked")
    
    def get_error_message(self):
        """Get error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=5):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_login_successful(self):
        """Check if login was successful by checking URL change"""
        time.sleep(2)  # Wait for navigation
        current_url = self.driver.current_url
        return "inventory" in current_url  # SauceDemo redirects to inventory page
    
    def is_login_page_loaded(self):
        """Check if login page is loaded"""
        return self.is_element_visible(self.LOGIN_CONTAINER)
    
    def take_login_screenshot(self):
        """Take screenshot of login page"""
        return self.take_screenshot("login_page")