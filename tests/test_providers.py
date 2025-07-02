#!/usr/bin/env python3
"""
Test script for multi-provider financial data system
"""

import sys
import os
# Add parent directory's src folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_data_providers import YahooFinanceProvider
from test_provider_system import TestMultiProviderFinancialData

def test_yahoo_finance():
    """Test Yahoo Finance provider directly"""
    print("🧪 Testing Yahoo Finance Provider...")
    provider = YahooFinanceProvider()
    
    # Test with a well-known stock
    result = provider.get_financial_data("AAPL")
    
    if result.startswith("Error:"):
        print(f"❌ Yahoo Finance test failed: {result}")
        return False
    else:
        print("✅ Yahoo Finance test passed!")
        print(f"📊 Sample data preview:\n{result[:300]}...")
        return True

def test_multi_provider_system():
    """Test the multi-provider system (with mock data for testing)"""
    print("\n🧪 Testing Multi-Provider System...")
    system = TestMultiProviderFinancialData()
    
    # Test provider status
    print("\n📋 Provider Status:")
    status = system.get_provider_status()
    print(status)
    
    # Test data retrieval
    print("🔍 Testing data retrieval for AAPL...")
    result = system.get_financial_data("AAPL")
    
    if result.startswith("Error:") or result.startswith("All providers failed"):
        print(f"❌ Multi-provider test failed: {result}")
        return False
    else:
        print("✅ Multi-provider test passed!")
        print(f"📊 Retrieved data:\n{result[:500]}...")
        return True

def test_multiple_stocks():
    """Test with multiple different stocks (using test system with mock fallback)"""
    print("\n🧪 Testing Multiple Stocks...")
    system = TestMultiProviderFinancialData()
    
    test_stocks = ["MSFT", "GOOGL", "TSLA"]
    results = {}
    
    for stock in test_stocks:
        print(f"🔍 Testing {stock}...")
        result = system.get_financial_data(stock)
        
        if result.startswith("Error:") or result.startswith("All providers failed"):
            print(f"❌ {stock}: {result[:100]}...")
            results[stock] = False
        else:
            print(f"✅ {stock}: Success!")
            results[stock] = True
    
    return results

def test_production_system_no_mock():
    """Test that production system never returns mock data"""
    print("\n🧪 Testing Production System (No Mock Data)...")
    from financial_data_providers import MultiProviderFinancialData
    
    system = MultiProviderFinancialData()
    
    # Check that mock provider is not included
    provider_names = system.get_active_provider_names()
    print(f"Production providers: {provider_names}")
    
    if "Mock Data Provider" in provider_names:
        print("❌ Production system contains mock data provider!")
        return False
    else:
        print("✅ Production system correctly excludes mock data")
        return True

def main():
    print("🚀 Financial Data Providers Test Suite")
    print("=" * 50)
    
    # Test individual provider
    yahoo_success = test_yahoo_finance()
    
    # Test multi-provider system
    multi_success = test_multi_provider_system()
    
    # Test multiple stocks
    stock_results = test_multiple_stocks()
    
    # Test production system has no mock data
    production_success = test_production_system_no_mock()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Yahoo Finance Direct: {'✅ PASS' if yahoo_success else '❌ FAIL'}")
    print(f"Multi-Provider System: {'✅ PASS' if multi_success else '❌ FAIL'}")
    print(f"Production No Mock: {'✅ PASS' if production_success else '❌ FAIL'}")
    
    print("\nStock Tests:")
    for stock, success in stock_results.items():
        print(f"  {stock}: {'✅ PASS' if success else '❌ FAIL'}")
    
    # Overall result
    all_stock_success = all(stock_results.values())
    overall_success = yahoo_success and multi_success and all_stock_success and production_success
    
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 Multi-provider system is working correctly!")
        print("💡 Ready to commit changes to repository.")
    else:
        print("\n⚠️  Some issues detected. Please review the errors above.")
    
    return overall_success

if __name__ == "__main__":
    main() 