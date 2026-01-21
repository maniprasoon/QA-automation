#!/usr/bin/env python3
"""
Complete Demo Test Runner for HCLTech QA Automation Project
"""

import os
import sys
import subprocess
from datetime import datetime

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import after path setup
from utilities.config import Config

def print_banner():
    """Print execution banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║      HCLTech QA Automation - Demo Test Suite          ║
    ║      Authentication Module Testing (SauceDemo)        ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)

def run_demo_tests():
    """Run all demo tests"""
    print("🚀 Starting HCLTech QA Automation Demo Tests")
    print("="*60)
    print(f"📁 Project Directory: {current_dir}")
    print(f"🌐 Testing Website: {Config.BASE_URL}")
    print(f"📊 Reports Directory: {Config.REPORTS_DIR}")
    print("="*60)
    
    # Create timestamp for report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = Config.REPORTS_DIR / f"hcl_demo_report_{timestamp}.html"
    
    # Run demo tests
    cmd = [
        sys.executable,
        "-m", "pytest",
        "tests/test_demo.py",
        "-v",
        "--tb=short",
        f"--html={report_file}",
        "--self-contained-html",
        "--capture=no"  # Show print statements in console
    ]
    
    print(f"\n📋 Test Command: {' '.join(cmd)}")
    print("\n" + "="*60)
    print("🏃 TEST EXECUTION STARTED")
    print("="*60)
    
    result = subprocess.run(cmd)
    
    print("\n" + "="*60)
    print("📊 TEST EXECUTION COMPLETED")
    print("="*60)
    
    # Print results
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print(f"⚠️  Some tests failed (Exit code: {result.returncode})")
    
    print(f"\n📈 Detailed HTML Report:")
    print(f"   file:///{report_file}")
    
    # Also show the default report location
    default_report = Config.REPORTS_DIR / "test_report.html"
    if default_report.exists():
        print(f"📊 Default Report (if generated):")
        print(f"   file:///{default_report}")
    
    print("\n" + "="*60)
    return result.returncode

if __name__ == "__main__":
    print_banner()
    exit_code = run_demo_tests()
    sys.exit(exit_code)