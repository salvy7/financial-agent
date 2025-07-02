#!/usr/bin/env python3
"""
Test runner for Financial Analysis System

Usage:
    python run_tests.py                 # Run all tests
    python run_tests.py providers       # Run provider tests
    python run_tests.py debug           # Run debug tests
"""

import sys
import os
import subprocess
from pathlib import Path

def run_test(test_name):
    """Run a specific test file"""
    test_file = Path("tests") / f"{test_name}.py"
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    print(f"🚀 Running {test_name}...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, str(test_file)], 
                              capture_output=False, 
                              cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ {test_name} completed successfully")
            return True
        else:
            print(f"❌ {test_name} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {test_name}: {e}")
        return False

def main():
    """Main test runner"""
    available_tests = {
        'providers': 'test_providers',
        'debug': 'debug_yfinance'
    }
    
    if len(sys.argv) == 1:
        # Run all tests
        print("🧪 Running All Tests")
        print("=" * 50)
        
        results = {}
        for test_name, test_file in available_tests.items():
            print(f"\n{'='*20} {test_name.upper()} TEST {'='*20}")
            results[test_name] = run_test(test_file)
        
        # Summary
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        all_passed = True
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test_name.ljust(15)}: {status}")
            if not passed:
                all_passed = False
        
        print("="*50)
        overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
        print(f"Overall: {overall_status}")
        
        return 0 if all_passed else 1
        
    elif len(sys.argv) == 2:
        # Run specific test
        test_name = sys.argv[1].lower()
        
        if test_name in available_tests:
            success = run_test(available_tests[test_name])
            return 0 if success else 1
        else:
            print(f"❌ Unknown test: {test_name}")
            print(f"Available tests: {', '.join(available_tests.keys())}")
            return 1
    else:
        print("Usage: python run_tests.py [test_name]")
        print(f"Available tests: {', '.join(available_tests.keys())}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 