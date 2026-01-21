from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.logger import get_logger

class BasePage:
    """Base class for all page objects with common utilities"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)
        self.wait = WebDriverWait(driver, 20)  # Explicit wait
    
    def find_element(self, locator, timeout=20):
        """Find element with explicit wait"""
        try:
            self.logger.log_debug(f"Finding element: {locator}")
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.log_error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator, timeout=20):
        """Find multiple elements with explicit wait"""
        try:
            self.logger.log_debug(f"Finding elements: {locator}")
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            self.logger.log_error(f"Elements not found: {locator}")
            raise
    
    def click_element(self, locator, timeout=20):
        """Click on element with explicit wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.log_debug(f"Clicked element: {locator}")
        except TimeoutException:
            self.logger.log_error(f"Element not clickable: {locator}")
            raise
    
    def enter_text(self, locator, text, timeout=20):
        """Enter text in element with explicit wait"""
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
            self.logger.log_debug(f"Entered text '{text}' in element: {locator}")
        except Exception as e:
            self.logger.log_error(f"Failed to enter text: {e}")
            raise
    
    def get_text(self, locator, timeout=20):
        """Get text from element"""
        try:
            element = self.find_element(locator, timeout)
            text = element.text
            self.logger.log_debug(f"Got text '{text}' from element: {locator}")
            return text
        except Exception as e:
            self.logger.log_error(f"Failed to get text: {e}")
            raise
    
    def is_element_visible(self, locator, timeout=10):
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, name=""):
        """Take screenshot and save to reports directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"screenshot_{name}_{timestamp}.png"
        screenshot_path = Config.REPORTS_DIR / screenshot_name
        
        self.driver.save_screenshot(str(screenshot_path))
        self.logger.log_info(f"Screenshot saved: {screenshot_name}")
        return screenshot_path