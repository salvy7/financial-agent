#!/usr/bin/env python3
"""
Debug script for yfinance issues
"""

import sys
import os
# Add parent directory's src folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import yfinance as yf
import pandas as pd

def debug_yfinance():
    print("🔍 Debugging Yahoo Finance...")
    
    try:
        # Test basic ticker creation
        print("1. Creating ticker object...")
        ticker = yf.Ticker("AAPL")
        print("✅ Ticker created successfully")
        
        # Test basic info
        print("\n2. Getting basic info...")
        try:
            info = ticker.info
            print(f"✅ Got info: {len(info)} fields")
            print(f"   Company name: {info.get('longName', 'N/A')}")
            print(f"   Symbol: {info.get('symbol', 'N/A')}")
        except Exception as e:
            print(f"❌ Info failed: {e}")
        
        # Test historical data with different periods
        print("\n3. Testing different historical periods...")
        periods = ["1d", "5d", "1mo", "3mo"]
        
        for period in periods:
            try:
                print(f"   Testing period: {period}")
                hist = ticker.history(period=period)
                if not hist.empty:
                    print(f"   ✅ {period}: Got {len(hist)} rows")
                    print(f"      Latest close: ${hist['Close'].iloc[-1]:.2f}")
                    break
                else:
                    print(f"   ❌ {period}: Empty data")
            except Exception as e:
                print(f"   ❌ {period}: {e}")
        
        # Test fast info (newer yfinance feature)
        print("\n4. Testing fast_info...")
        try:
            fast_info = ticker.fast_info
            print(f"✅ Fast info available")
            print(f"   Last price: ${fast_info.get('lastPrice', 'N/A')}")
            print(f"   Market cap: {fast_info.get('marketCap', 'N/A')}")
        except Exception as e:
            print(f"❌ Fast info failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return False

def test_alternative_approach():
    """Test alternative approach using different methods"""
    print("\n🔧 Testing alternative approaches...")
    
    try:
        # Test with download function
        print("1. Testing yf.download...")
        data = yf.download("AAPL", period="5d", progress=False)
        if not data.empty:
            print(f"✅ Download successful: {len(data)} rows")
            print(f"   Latest close: ${data['Close'].iloc[-1]:.2f}")
            return data
        else:
            print("❌ Download returned empty data")
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
    
    return None

def main():
    print("🚀 Yahoo Finance Debug Suite")
    print("=" * 40)
    
    # Test basic yfinance
    success = debug_yfinance()
    
    # Test alternative approach
    data = test_alternative_approach()
    
    if success or data is not None:
        print("\n✅ At least one method works!")
        return True
    else:
        print("\n❌ All methods failed - Yahoo Finance may be down")
        return False

if __name__ == "__main__":
    main() 