import json
import os
from utilities.config import Config

class TestDataReader:
    """Utility class to read test data from various sources"""
    
    @staticmethod
    def load_json_data(file_path):
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Test data file not found: {file_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in file: {file_path}")
    
    @staticmethod
    def get_credentials():
        """Get all credentials from credentials file"""
        credentials_file = Config.CREDENTIALS_FILE
        return TestDataReader.load_json_data(credentials_file)
    
    @staticmethod
    def get_valid_credentials():
        """Get valid credentials for login"""
        data = TestDataReader.get_credentials()
        return data['valid_credentials']
    
    @staticmethod
    def get_invalid_credentials():
        """Get list of invalid credentials for negative testing"""
        data = TestDataReader.get_credentials()
        return data['invalid_credentials']
    
    @staticmethod
    def get_password_reset_data():
        """Get password reset test data"""
        data = TestDataReader.get_credentials()
        return data['password_reset_emails']
    
    @staticmethod
    def get_test_config():
        """Get test configuration"""
        return TestDataReader.load_json_data(Config.TEST_CONFIG_FILE)