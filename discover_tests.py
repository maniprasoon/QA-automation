#!/usr/bin/env python3
"""
Script to discover and list all tests
"""

import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest

print("🔍 DISCOVERING TESTS")
print("="*60)

# Run pytest in collection mode
args = [
    "tests/",
    "--collect-only",
    "-q"  # Quiet mode
]

print(f"Running: pytest {' '.join(args)}")
print()

try:
    # Collect tests
    exit_code = pytest.main(args)
    
    if exit_code == 0:
        print("\n✅ Tests discovered successfully")
    else:
        print(f"\n❌ Test discovery failed with code: {exit_code}")
        
except Exception as e:
    print(f"\n💥 Error during test discovery: {e}")