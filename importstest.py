#!/usr/bin/env python3
"""
Script to verify all imports work correctly
"""

import sys
import os

print("🔍 VERIFYING IMPORTS...")
print("="*60)

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print(f"📁 Project Root: {PROJECT_ROOT}")
print(f"📁 Python Path:")
for i, path in enumerate(sys.path[:5]):  # Show first 5 paths
    print(f"  {i+1}. {path}")

print("\n" + "="*60)
print("TESTING IMPORTS:")

modules_to_test = [
    ("utilities.config", "Config"),
    ("utilities.logger", "get_logger"),
    ("utilities.data_reader", "TestDataReader"),
    ("pages.base_page", "BasePage"),
    ("pages.login_page", "LoginPage"),
    ("pages.password_reset_page", "PasswordResetPage"),
]

all_ok = True
for module_name, class_name in modules_to_test:
    try:
        module = __import__(module_name, fromlist=[class_name])
        if hasattr(module, class_name):
            print(f"✅ {module_name}.{class_name}")
        else:
            print(f"❌ {module_name}.{class_name} - Not found")
            all_ok = False
    except ImportError as e:
        print(f"❌ {module_name}.{class_name} - {e}")
        all_ok = False

print("\n" + "="*60)
if all_ok:
    print("✅ ALL IMPORTS SUCCESSFUL!")
else:
    print("❌ SOME IMPORTS FAILED")

# Test creating directories
from utilities.config import Config
print("\n📁 TESTING DIRECTORY CREATION:")
for dir_name, dir_path in [
    ("Test Data", Config.TEST_DATA_DIR),
    ("Reports", Config.REPORTS_DIR),
    ("Logs", Config.LOGS_DIR)
]:
    dir_path.mkdir(exist_ok=True)
    print(f"✅ {dir_name}: {dir_path}")