import pytest
import sys
import os
from pathlib import Path

# ============================================================
# CRITICAL: Add project root to Python path
# ============================================================
# Get the absolute path of the project root (two levels up from conftest.py)
PROJECT_ROOT = Path(__file__).parent.parent

# Add project root to Python path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Now import project modules
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from utilities.config import Config
    from utilities.logger import get_logger
    
    print(f"✅ conftest.py: Successfully imported modules from {PROJECT_ROOT}")
except ImportError as e:
    print(f"❌ conftest.py: Import Error - {e}")
    print(f"📁 Project Root: {PROJECT_ROOT}")
    print(f"📁 sys.path: {sys.path}")
    raise

logger = get_logger("TestFixture")

@pytest.fixture(scope="session")
def config():
    """Load configuration for the test session"""
    try:
        credentials, test_config = Config.load_test_data()
        return {
            "credentials": credentials,
            "config": test_config
        }
    except Exception as e:
        logger.log_error(f"Failed to load config: {e}")
        # Return default config if file loading fails
        return {
            "credentials": {
                "valid_credentials": {"username": "test", "password": "test"},
                "invalid_credentials": []
            },
            "config": {"test_environment": "default"}
        }

@pytest.fixture(scope="function")
def driver(config):
    """Setup and teardown WebDriver instance for each test"""
    browser = Config.BROWSER
    headless = Config.HEADLESS
    
    logger.log_info(f"Initializing {browser} browser (Headless: {headless})")
    
    driver_instance = None
    
    try:
        if browser.lower() == "chrome":
            options = Options()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-gpu")
            
            # Initialize Chrome driver
            driver_instance = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
        
        elif browser.lower() == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            
            # Initialize Firefox driver
            driver_instance = webdriver.Firefox(
                service=Service(GeckoDriverManager().install()),
                options=options
            )
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Set implicit wait
        driver_instance.implicitly_wait(Config.IMPLICIT_WAIT)
        
        # Maximize window
        driver_instance.maximize_window()
        
        logger.log_info(f"{browser} browser initialized successfully")
        
        yield driver_instance
        
    except Exception as e:
        logger.log_error(f"Failed to initialize browser: {e}")
        pytest.fail(f"Browser initialization failed: {e}")
    
    finally:
        # Teardown
        if driver_instance:
            logger.log_info("Closing browser")
            driver_instance.quit()

@pytest.fixture(scope="function")
def login_page(driver):
    """Fixture to provide LoginPage instance"""
    from pages.login_page import LoginPage
    return LoginPage(driver)

@pytest.fixture(scope="function")
def password_reset_page(driver):
    """Fixture to provide PasswordResetPage instance"""
    from pages.password_reset_page import PasswordResetPage
    return PasswordResetPage(driver)

@pytest.fixture(scope="function", autouse=True)
def log_test_name(request):
    """Automatically log test start and end"""
    test_name = request.node.name
    logger = get_logger(test_name)
    logger.log_info(f"Starting test: {test_name}")
    
    yield
    
    logger.log_info(f"Completed test: {test_name}")

# Hook for pytest-html report
def pytest_html_report_title(report):
    """Set HTML report title"""
    report.title = "HCLTech QA Automation Test Report"

def pytest_configure(config):
    """Configure pytest options"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "login: mark test as login test"
    )
    config.addinivalue_line(
        "markers", "password_reset: mark test as password reset test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
def pytest_configure(config):
    """Configure pytest options"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "login: mark test as login test"
    )
    config.addinivalue_line(
        "markers", "password_reset: mark test as password reset test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "demo: mark test as demo test"  # ADD THIS LINE
    )