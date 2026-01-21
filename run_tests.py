#!/usr/bin/env python3
"""
Main Test Runner for HCLTech QA Automation Project
Production-ready test execution with comprehensive reporting
"""

import sys
import os
import subprocess
import argparse
from datetime import datetime

# ============================================================
# Add project root to Python path BEFORE any imports
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ============================================================
# Import project modules
# ============================================================
try:
    from utilities.config import Config
    from utilities.logger import get_logger
    print("✅ Successfully imported project modules")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure you are running from the project root directory.")
    sys.exit(1)

logger = get_logger("HCLTestRunner")

def print_hcltech_banner():
    """Print HCLTech branded execution banner"""
    banner = r"""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║                     HCLTech QA Automation Framework                   ║
    ║                 Enterprise Authentication Module Testing              ║
    ║                                                                       ║
    ║  Features: Page Object Model • Data-Driven Testing • Parallel Exec    ║
    ║            Comprehensive Logging • HTML Reports • Screenshot Capture  ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def setup_environment():
    """Setup test environment and create necessary directories"""
    print("\n🔧 Setting up test environment...")
    
    directories = [Config.REPORTS_DIR, Config.LOGS_DIR]
    for directory in directories:
        try:
            directory.mkdir(exist_ok=True)
            print(f"   ✅ Created/verified: {directory}")
        except Exception as e:
            print(f"   ⚠️  Could not create {directory}: {e}")
    
    print("✅ Environment setup complete")

def display_configuration():
    """Display current test configuration"""
    print("\n⚙️  TEST CONFIGURATION")
    print("-" * 50)
    
    config_info = {
        "Test Environment": "SauceDemo (Public Demo Site)",
        "Browser": Config.BROWSER,
        "Headless Mode": "Yes" if Config.HEADLESS else "No",
        "Base URL": Config.BASE_URL,
        "Implicit Wait": f"{Config.IMPLICIT_WAIT} seconds",
        "Reports Directory": str(Config.REPORTS_DIR),
        "Test Cases": "12+ (Login, Password Reset, Validation)"
    }
    
    for key, value in config_info.items():
        print(f"{key:25}: {value}")
    
    print("-" * 50)

def run_tests(test_type="all", parallel=False, headless=False, browser=None):
    """
    Execute test cases with comprehensive reporting
    
    Args:
        test_type: Type of tests to run (all, login, reset, demo)
        parallel: Run tests in parallel
        headless: Run browser in headless mode
        browser: Browser to use (chrome, firefox)
    """
    
    # Setup environment
    setup_environment()
    
    # Set environment variables
    env_vars = os.environ.copy()
    if browser:
        env_vars["BROWSER"] = browser
    if headless:
        env_vars["HEADLESS"] = "True"
    
    # Add project root to Python path
    env_vars["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + env_vars.get("PYTHONPATH", "")
    
    # Create timestamp for unique report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Build pytest command
    cmd = [
        sys.executable,
        "-m", "pytest",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback
        f"--html={Config.REPORTS_DIR}/hcl_test_report_{timestamp}.html",
        "--self-contained-html",
        f"--log-file={Config.LOGS_DIR}/execution_{timestamp}.log",
        "--log-file-level=INFO",
        "--capture=no"  # Show print statements
    ]
    
    # Add parallel execution if requested
    if parallel:
        cmd.extend(["-n", "auto"])
        print("   🔄 Running tests in parallel mode")
    
    # Determine test path based on test_type
    if test_type == "login":
        cmd.append("tests/test_login.py")
        test_description = "Login Functionality Tests"
    elif test_type == "reset":
        cmd.append("tests/test_password_reset.py")
        test_description = "Password Reset Tests"
    elif test_type == "demo":
        cmd.append("tests/test_demo.py")
        test_description = "Demo Tests (SauceDemo Website)"
    elif test_type == "smoke":
        cmd.extend(["-m", "smoke"])
        test_description = "Smoke Tests"
    else:
        cmd.append("tests/")
        test_description = "All Tests (Complete Test Suite)"
    
    print(f"\n🚀 EXECUTING: {test_description}")
    print("-" * 50)
    
    try:
        # Execute tests
        result = subprocess.run(cmd, env=env_vars)
        
        # Display results
        print("\n" + "="*60)
        print("📊 TEST EXECUTION RESULTS")
        print("="*60)
        
        if result.returncode == 0:
            print("✅ SUCCESS: All tests passed!")
        else:
            print(f"⚠️  COMPLETED: Some tests failed (Exit code: {result.returncode})")
        
        # Show report location
        report_file = Config.REPORTS_DIR / f"hcl_test_report_{timestamp}.html"
        print(f"\n📈 Detailed Report: file:///{report_file}")
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ ERROR: Failed to execute tests - {e}")
        return 1

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(
        description="HCLTech QA Automation Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                        # Run all tests
  %(prog)s --test-type login      # Run login tests only
  %(prog)s --test-type demo       # Run demo tests (recommended first)
  %(prog)s --parallel             # Run tests in parallel
  %(prog)s --headless             # Run in headless mode
  %(prog)s --browser firefox      # Run with Firefox
  %(prog)s --help                 # Show this help message

Test Types:
  all     - Run all test suites (default)
  login   - Login functionality tests only
  reset   - Password reset tests only
  demo    - Demo tests against SauceDemo website
  smoke   - Smoke tests only
        """
    )
    
    parser.add_argument(
        "--test-type",
        choices=["all", "login", "reset", "demo", "smoke"],
        default="demo",  # Default to demo for safety
        help="Type of tests to run (default: demo)"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel for faster execution"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (no GUI)"
    )
    
    parser.add_argument(
        "--browser",
        choices=["chrome", "firefox"],
        default=None,
        help="Browser to use for tests (default: chrome)"
    )
    
    parser.add_argument(
        "--list-tests",
        action="store_true",
        help="List all available test cases"
    )
    
    parser.add_argument(
        "--generate-report",
        action="store_true",
        help="Generate project summary report"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_hcltech_banner()
    
    # Display configuration
    display_configuration()
    
    # Generate report if requested
    if args.generate_report:
        print("\n📋 Generating project summary report...")
        subprocess.run([sys.executable, "generate_report.py"])
        return 0
    
    # List tests if requested
    if args.list_tests:
        print("\n📋 AVAILABLE TEST CASES")
        print("-" * 40)
        
        test_suites = {
            "Login Tests (7)": [
                "test_valid_login",
                "test_invalid_login_attempts (data-driven)",
                "test_login_page_elements_visibility",
                "test_password_masking",
                "test_forgot_password_link",
                "test_empty_credentials_validation",
                "test_max_login_attempts"
            ],
            "Password Reset Tests (5)": [
                "test_password_reset_page_elements",
                "test_password_reset_requests (data-driven)",
                "test_empty_email_validation",
                "test_back_to_login_navigation",
                "test_invalid_email_format"
            ],
            "Demo Tests (5)": [
                "test_navigate_to_login_page",
                "test_login_form_elements",
                "test_valid_login_demo",
                "test_invalid_login_demo",
                "test_empty_login"
            ]
        }
        
        for suite_name, tests in test_suites.items():
            print(f"\n{suite_name}:")
            for test in tests:
                print(f"  • {test}")
        
        print(f"\n📊 Total: 17+ test cases")
        return 0
    
    # Show execution parameters
    print("\n🏃 EXECUTION PARAMETERS")
    print("-" * 40)
    
    params = {
        "Test Type": args.test_type,
        "Parallel Execution": "Yes" if args.parallel else "No",
        "Headless Mode": "Yes" if args.headless else "No",
        "Browser": args.browser if args.browser else "chrome (default)"
    }
    
    for key, value in params.items():
        print(f"{key:20}: {value}")
    
    print("-" * 40)
    
    # Run tests
    exit_code = run_tests(
        test_type=args.test_type,
        parallel=args.parallel,
        headless=args.headless,
        browser=args.browser
    )
    
    # Final message
    print("\n" + "="*60)
    if exit_code == 0:
        print("🎉 HCLTech Automation Project - TEST EXECUTION SUCCESSFUL")
    elif exit_code == 130:
        print("⏹️  Test execution interrupted")
    else:
        print(f"⚠️  HCLTech Automation Project - TEST EXECUTION COMPLETED")
    print("="*60)
    
    return exit_code

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)