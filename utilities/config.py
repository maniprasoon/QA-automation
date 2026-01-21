import os
from pathlib import Path
import json

class Config:
    """Configuration management for the automation framework"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    TEST_DATA_DIR = BASE_DIR / "test_data"
    REPORTS_DIR = BASE_DIR / "reports"
    LOGS_DIR = BASE_DIR / "reports" / "logs"
    
    # Browser configuration
    BROWSER = "chrome"  # chrome, firefox, edge
    HEADLESS = False  # Set to True for CI/CD pipelines
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    
    # ============================================================
    # 🎯 IMPORTANT: Change these URLs to real test websites
    # ============================================================
    
    # Option 1: SauceDemo (Free demo e-commerce site - RECOMMENDED)
    BASE_URL = "https://www.saucedemo.com"
    LOGIN_URL = f"{BASE_URL}/"
    PASSWORD_RESET_URL = f"{BASE_URL}/"  # Note: SauceDemo doesn't have password reset
    
    # Option 2: OrangeHRM Demo (Free HR management demo)
    # BASE_URL = "https://opensource-demo.orangehrmlive.com"
    # LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"
    # PASSWORD_RESET_URL = f"{BASE_URL}/web/index.php/auth/requestPasswordResetCode"
    
    # Option 3: Your local application (if testing locally)
    # BASE_URL = "http://localhost:3000"
    # LOGIN_URL = f"{BASE_URL}/login"
    # PASSWORD_RESET_URL = f"{BASE_URL}/forgot-password"
    
    # Test Data Files
    CREDENTIALS_FILE = TEST_DATA_DIR / "credentials.json"
    TEST_CONFIG_FILE = TEST_DATA_DIR / "test_config.json"
    
    # Create directories if they don't exist
    for directory in [TEST_DATA_DIR, REPORTS_DIR, LOGS_DIR]:
        directory.mkdir(exist_ok=True)
    
    @classmethod
    def load_test_data(cls):
        """Load test data from JSON files"""
        try:
            with open(cls.CREDENTIALS_FILE, 'r') as f:
                credentials = json.load(f)
            with open(cls.TEST_CONFIG_FILE, 'r') as f:
                config = json.load(f)
            return credentials, config
        except FileNotFoundError:
            # Return default data if files don't exist
            print(f"⚠️  Config files not found. Using default data.")
            return cls.get_default_data()
    
    @classmethod
    def get_default_data(cls):
        """Return default test data"""
        default_credentials = {
            "valid_credentials": {
                "username": "standard_user",
                "password": "secret_sauce"
            },
            "invalid_credentials": [
                {
                    "username": "locked_out_user",
                    "password": "secret_sauce",
                    "expected_error": "Epic sadface: Sorry, this user has been locked out."
                },
                {
                    "username": "",
                    "password": "secret_sauce",
                    "expected_error": "Epic sadface: Username is required"
                },
                {
                    "username": "standard_user",
                    "password": "",
                    "expected_error": "Epic sadface: Password is required"
                }
            ],
            "password_reset_emails": [
                {
                    "email": "test@example.com",
                    "expected_result": "success"
                }
            ]
        }
        
        default_config = {
            "test_environment": "demo",
            "max_login_attempts": 3,
            "password_reset_timeout": 60,
            "screenshot_on_failure": True,
            "retry_failed_tests": 2
        }
        
        return default_credentials, default_config