#!/usr/bin/env python3
"""
Test script to demonstrate financial data caching functionality
"""

import sys
import time
sys.path.append('src')

from financial_agents import FinancialAnalysisAgent
from langchain_community.llms import Ollama

def test_caching():
    """Test the caching functionality"""
    print("🧪 Testing Financial Data Caching")
    print("=" * 50)
    
    # Initialize the agent with Llama 3.1
    llm = Ollama(
        model="llama3.1:8b",
        temperature=0.7,
        base_url="http://localhost:11434"
    )
    
    agent = FinancialAnalysisAgent(llm)
    
    # Test symbol
    symbol = "AAPL"
    
    print(f"\n📊 First request for {symbol}:")
    print("-" * 30)
    start_time = time.time()
    result1 = agent.get_financial_data(symbol)
    time1 = time.time() - start_time
    print(f"⏱️  Time taken: {time1:.2f} seconds")
    print(f"📄 Data length: {len(result1)} characters")
    
    print(f"\n📊 Second request for {symbol} (should use cache):")
    print("-" * 30)
    start_time = time.time()
    result2 = agent.get_financial_data(symbol)
    time2 = time.time() - start_time
    print(f"⏱️  Time taken: {time2:.2f} seconds")
    print(f"📄 Data length: {len(result2)} characters")
    
    print(f"\n📊 Third request for {symbol} (should use cache):")
    print("-" * 30)
    start_time = time.time()
    result3 = agent.get_financial_data(symbol)
    time3 = time.time() - start_time
    print(f"⏱️  Time taken: {time3:.2f} seconds")
    print(f"📄 Data length: {len(result3)} characters")
    
    # Test cache status
    print(f"\n📋 Cache Status:")
    print("-" * 30)
    cache_status = agent.get_cache_status()
    print(cache_status)
    
    # Test with different symbol
    print(f"\n📊 Request for different symbol (MSFT):")
    print("-" * 30)
    start_time = time.time()
    result_msft = agent.get_financial_data("MSFT")
    time_msft = time.time() - start_time
    print(f"⏱️  Time taken: {time_msft:.2f} seconds")
    print(f"📄 Data length: {len(result_msft)} characters")
    
    # Show final cache status
    print(f"\n📋 Final Cache Status:")
    print("-" * 30)
    final_cache_status = agent.get_cache_status()
    print(final_cache_status)
    
    # Performance comparison
    print(f"\n📈 Performance Comparison:")
    print("-" * 30)
    print(f"First request (API call): {time1:.2f} seconds")
    print(f"Second request (cached):  {time2:.2f} seconds")
    print(f"Third request (cached):   {time3:.2f} seconds")
    print(f"MSFT request (API call):  {time_msft:.2f} seconds")
    
    if time2 < time1 * 0.1:  # Cache should be at least 10x faster
        print(f"✅ Caching working: {time1/time2:.1f}x speedup")
    else:
        print(f"⚠️  Cache performance: {time1/time2:.1f}x speedup")
    
    # Test cache clearing
    print(f"\n🗑️  Testing cache clearing:")
    print("-" * 30)
    clear_result = agent.clear_cache()
    print(clear_result)
    
    # Verify cache is cleared
    final_status = agent.get_cache_status()
    print(f"\n📋 Cache Status After Clearing:")
    print("-" * 30)
    print(final_status)

if __name__ == "__main__":
    test_caching() 