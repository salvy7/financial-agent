"""
Enhanced Financial Data Providers with Multiple APIs
Provides alternatives to Alpha Vantage with better rate limits
"""

import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import os
from dotenv import load_dotenv
# Note: SimpleFallbackProvider moved to tests/test_provider_system.py for test-only use

# Alpha Vantage imports
try:
    from alpha_vantage.timeseries import TimeSeries
    from alpha_vantage.techindicators import TechIndicators
    ALPHA_VANTAGE_AVAILABLE = True
except ImportError:
    ALPHA_VANTAGE_AVAILABLE = False

load_dotenv()

class YahooFinanceProvider:
    """
    Yahoo Finance provider - Most reliable, virtually unlimited requests
    """
    
    def __init__(self):
        self.name = "Yahoo Finance"
        self.rate_limit = "Virtually unlimited"
    
    def get_financial_data(self, symbol: str) -> str:
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Try different approaches to get data
            hist = None
            fast_info = None
            info = {}
            
            # First try fast_info (more reliable)
            try:
                fast_info = ticker.fast_info
                if fast_info and fast_info.get('lastPrice'):
                    print(f"✅ Fast info available for {symbol}")
                    print(f"   Last Price: ${fast_info.get('lastPrice')}")
                else:
                    print(f"⚠️  Fast info available but no lastPrice for {symbol}")
                    fast_info = None
            except Exception as e:
                print(f"Warning: Fast info failed for {symbol}: {e}")
                fast_info = None
            
            # Try to get historical data with shorter periods first
            for period in ["5d", "1mo", "3mo", "1y"]:
                try:
                    print(f"Trying {period} historical data for {symbol}...")
                    hist = ticker.history(period=period)
                    if not hist.empty:
                        print(f"✅ Got {len(hist)} days of data")
                        break
                    else:
                        print(f"❌ Empty data for {period}")
                except Exception as e:
                    print(f"❌ Failed {period}: {e}")
                    time.sleep(0.5)  # Small delay between attempts
            
            # If no historical data, try yf.download as fallback
            if hist is None or hist.empty:
                try:
                    print(f"Trying yf.download for {symbol}...")
                    hist = yf.download(symbol, period="5d", progress=False)
                    if not hist.empty:
                        print(f"✅ Download successful: {len(hist)} rows")
                except Exception as e:
                    print(f"❌ Download failed: {e}")
            
            # If we have fast_info, we can proceed even without historical data
            if fast_info and fast_info.get('lastPrice'):
                print(f"✅ Using fast_info data for {symbol}")
            # If no fast_info and no historical data, return error
            elif (hist is None or hist.empty):
                return f"Error: No data available for {symbol}. Yahoo Finance may be rate-limited. Please try again later."
            
            # Get company info (with error handling)
            company_name = symbol
            sector = market_cap = pe_ratio = dividend_yield = beta = 'N/A'
            
            try:
                info = ticker.info
                company_name = info.get('longName', symbol)
                sector = info.get('sector', 'N/A')
                market_cap = info.get('marketCap', 'N/A')
                pe_ratio = info.get('trailingPE', 'N/A')
                dividend_yield = info.get('dividendYield', 'N/A')
                beta = info.get('beta', 'N/A')
            except Exception as e:
                print(f"Warning: Company info failed: {e}")
                # Use fast_info for company data if available
                if fast_info:
                    if fast_info.get('marketCap'):
                        market_cap = fast_info.get('marketCap')
                    # Note: fast_info doesn't have P/E ratio or dividend yield
            
            # Format response
            response = f"Financial Data for {symbol} ({company_name}):\n"
            response += f"Data Source: {self.name}"
            if fast_info and fast_info.get('lastPrice'):
                response += " (Real-time via fast_info)"
            response += f"\nSector: {sector}\n\n"
            
            # Use fast_info if available, otherwise use historical data
            if fast_info and fast_info.get('lastPrice'):
                response += f"Latest Trading Data (Real-time):\n"
                response += f"Current Price: ${fast_info.get('lastPrice'):.2f}\n"
                
                # Add more fast_info fields if available
                if fast_info.get('dayHigh'):
                    response += f"Day High: ${fast_info.get('dayHigh'):.2f}\n"
                if fast_info.get('dayLow'):
                    response += f"Day Low: ${fast_info.get('dayLow'):.2f}\n"
                if fast_info.get('open'):
                    response += f"Open: ${fast_info.get('open'):.2f}\n"
                if fast_info.get('lastVolume'):
                    response += f"Volume: {fast_info.get('lastVolume'):,.0f}\n"
                if fast_info.get('previousClose'):
                    response += f"Previous Close: ${fast_info.get('previousClose'):.2f}\n"
                    # Calculate change
                    current = fast_info.get('lastPrice')
                    prev_close = fast_info.get('previousClose')
                    if prev_close > 0:
                        change_pct = ((current - prev_close) / prev_close) * 100
                        response += f"Change: {change_pct:.2f}%\n"
                
                # Add fundamental data from fast_info if available
                if fast_info.get('marketCap'):
                    response += f"Market Cap: ${fast_info.get('marketCap'):,.0f}\n"
                if fast_info.get('fiftyDayAverage'):
                    response += f"50-day Average: ${fast_info.get('fiftyDayAverage'):.2f}\n"
                if fast_info.get('twoHundredDayAverage'):
                    response += f"200-day Average: ${fast_info.get('twoHundredDayAverage'):.2f}\n"
                if fast_info.get('yearChange'):
                    response += f"Year Change: {fast_info.get('yearChange'):.2f}%\n"
            
            # Add historical data analysis if available
            if hist is not None and not hist.empty:
                latest_data = hist.tail(1).iloc[0]
                
                if not (fast_info and fast_info.get('lastPrice')):
                    # Only show this if we don't have fast_info
                    response += f"Latest Trading Data ({latest_data.name.strftime('%Y-%m-%d')}):\n"
                    response += f"Open: ${latest_data['Open']:.2f}\n"
                    response += f"High: ${latest_data['High']:.2f}\n"
                    response += f"Low: ${latest_data['Low']:.2f}\n"
                    response += f"Close: ${latest_data['Close']:.2f}\n"
                    response += f"Volume: {latest_data['Volume']:,.0f}\n"
                
                # Calculate technical indicators
                hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
                hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
                
                # RSI calculation
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                hist['RSI'] = 100 - (100 / (1 + rs))
                
                # Performance metrics
                if len(hist) > 1:
                    week_ago = hist.tail(5).iloc[0]['Close'] if len(hist) >= 5 else hist.iloc[0]['Close']
                    month_ago = hist.tail(22).iloc[0]['Close'] if len(hist) >= 22 else hist.iloc[0]['Close']
                    
                    response += f"\nPerformance:\n"
                    if len(hist) >= 5:
                        response += f"1 Week Change: {((latest_data['Close'] / week_ago - 1) * 100):.2f}%\n"
                    if len(hist) >= 22:
                        response += f"1 Month Change: {((latest_data['Close'] / month_ago - 1) * 100):.2f}%\n"
                    if len(hist) >= 252:
                        year_ago = hist.iloc[0]['Close']
                        response += f"1 Year Change: {((latest_data['Close'] / year_ago - 1) * 100):.2f}%\n"
                
                # Technical indicators
                response += f"\nTechnical Indicators:\n"
                sma_20 = hist['SMA_20'].iloc[-1]
                sma_50 = hist['SMA_50'].iloc[-1]
                rsi = hist['RSI'].iloc[-1]
                
                if pd.notna(sma_20):
                    response += f"20-day SMA: ${sma_20:.2f}\n"
                if pd.notna(sma_50):
                    response += f"50-day SMA: ${sma_50:.2f}\n"
                if pd.notna(rsi):
                    response += f"14-day RSI: {rsi:.2f}\n"
            
            # Fundamental data
            response += f"\nFundamental Data:\n"
            if market_cap != 'N/A' and isinstance(market_cap, (int, float)):
                response += f"Market Cap: ${market_cap:,.0f}\n"
            if pe_ratio != 'N/A' and isinstance(pe_ratio, (int, float)):
                response += f"P/E Ratio: {pe_ratio:.2f}\n"
            if dividend_yield != 'N/A' and isinstance(dividend_yield, (int, float)):
                response += f"Dividend Yield: {dividend_yield*100:.2f}%\n"
            if beta != 'N/A' and isinstance(beta, (int, float)):
                response += f"Beta: {beta:.2f}\n"
            
            # Add note if using fast_info without historical data
            if fast_info and fast_info.get('lastPrice') and (hist is None or hist.empty):
                response += f"\n📊 Note: Using real-time data. Historical analysis not available due to rate limits."
            
            return response
            
        except Exception as e:
            return f"Error fetching data for {symbol} from Yahoo Finance: {str(e)}"

class PolygonProvider:
    """
    Polygon.io provider - 5 API calls per minute free tier
    """
    
    def __init__(self):
        self.api_key = os.getenv('POLYGON_API_KEY', '')
        self.base_url = "https://api.polygon.io"
        self.name = "Polygon.io"
        self.rate_limit = "5 calls/minute (free)"
    
    def get_financial_data(self, symbol: str) -> str:
        if not self.api_key:
            return "Error: POLYGON_API_KEY not found in environment variables."
        
        try:
            # Get previous close
            url = f"{self.base_url}/v2/aggs/ticker/{symbol}/prev"
            params = {"apikey": self.api_key}
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                return f"Error: Failed to fetch data from Polygon.io (Status: {response.status_code})"
            
            data = response.json()
            if data.get('status') != 'OK' or not data.get('results'):
                return f"Error: No data available for {symbol} from Polygon.io"
            
            result = data['results'][0]
            
            response_text = f"Financial Data for {symbol}:\n"
            response_text += f"Data Source: {self.name}\n\n"
            response_text += f"Previous Close Data:\n"
            response_text += f"Open: ${result['o']:.2f}\n"
            response_text += f"High: ${result['h']:.2f}\n"
            response_text += f"Low: ${result['l']:.2f}\n"
            response_text += f"Close: ${result['c']:.2f}\n"
            response_text += f"Volume: {result['v']:,.0f}\n"
            
            return response_text
            
        except Exception as e:
            return f"Error fetching data from Polygon.io: {str(e)}"

class FinnhubProvider:
    """
    Finnhub provider - 60 API calls per minute free tier
    """
    
    def __init__(self):
        self.api_key = os.getenv('FINNHUB_API_KEY', '')
        self.base_url = "https://finnhub.io/api/v1"
        self.name = "Finnhub"
        self.rate_limit = "60 calls/minute (free)"
    
    def get_financial_data(self, symbol: str) -> str:
        if not self.api_key:
            return "Error: FINNHUB_API_KEY not found in environment variables."
        
        try:
            # Get quote data
            url = f"{self.base_url}/quote"
            params = {"symbol": symbol, "token": self.api_key}
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                return f"Error: Failed to fetch data from Finnhub (Status: {response.status_code})"
            
            data = response.json()
            
            response_text = f"Financial Data for {symbol}:\n"
            response_text += f"Data Source: {self.name}\n\n"
            response_text += f"Real-time Quote:\n"
            response_text += f"Current Price: ${data.get('c', 0):.2f}\n"
            response_text += f"High (Day): ${data.get('h', 0):.2f}\n"
            response_text += f"Low (Day): ${data.get('l', 0):.2f}\n"
            response_text += f"Open: ${data.get('o', 0):.2f}\n"
            response_text += f"Previous Close: ${data.get('pc', 0):.2f}\n"
            
            # Calculate change
            current = data.get('c', 0)
            previous = data.get('pc', 0)
            if previous > 0:
                change_pct = ((current - previous) / previous) * 100
                response_text += f"Change: {change_pct:.2f}%\n"
            
            return response_text
            
        except Exception as e:
            return f"Error fetching data from Finnhub: {str(e)}"

class AlphaVantageProvider:
    """
    Alpha Vantage provider - 25 API calls per day free tier
    """
    
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')  # Use demo key as fallback
        self.name = "Alpha Vantage"
        self.rate_limit = "25 calls/day (free) or demo key (limited)"
        
        if not ALPHA_VANTAGE_AVAILABLE:
            raise ImportError("Alpha Vantage library not installed. Run: pip install alpha_vantage")
        
        self.ts = TimeSeries(key=self.api_key, output_format='pandas')
        self.ti = TechIndicators(key=self.api_key, output_format='pandas')
    
    def get_financial_data(self, symbol: str) -> str:
        try:
            # Add delay to avoid rate limiting
            time.sleep(1)
            
            # Get daily time series data
            data, meta_data = self.ts.get_daily(symbol=symbol, outputsize='compact')
            
            if data.empty:
                return f"Error: No data available for {symbol} from Alpha Vantage"
            
            # Get technical indicators
            try:
                sma_20, _ = self.ti.get_sma(symbol=symbol, interval='daily', time_period=20)
            except Exception as e:
                sma_20 = pd.DataFrame()
                print(f"Warning: Could not fetch SMA data: {str(e)}")
            
            try:
                rsi, _ = self.ti.get_rsi(symbol=symbol, interval='daily', time_period=14)
            except Exception as e:
                rsi = pd.DataFrame()
                print(f"Warning: Could not fetch RSI data: {str(e)}")
            
            # Format the response
            response = f"Financial Data for {symbol}:\n"
            response += f"Data Source: {self.name}\n\n"
            
            if not data.empty:
                latest_data = data.iloc[0]
                response += f"Latest Trading Data:\n"
                response += f"Date: {latest_data.name.strftime('%Y-%m-%d')}\n"
                response += f"Open: ${latest_data['1. open']:.2f}\n"
                response += f"High: ${latest_data['2. high']:.2f}\n"
                response += f"Low: ${latest_data['3. low']:.2f}\n"
                response += f"Close: ${latest_data['4. close']:.2f}\n"
                response += f"Volume: {latest_data['5. volume']:,.0f}\n"
                
                # Calculate price change
                if len(data) > 1:
                    price_change = ((latest_data['4. close'] / data.iloc[-1]['4. close'] - 1) * 100)
                    response += f"Price Change: {price_change:.2f}%\n"
                
                # Add technical indicators if available
                if not sma_20.empty:
                    response += f"\nTechnical Indicators:\n"
                    response += f"20-day SMA: ${sma_20.iloc[0]['SMA']:.2f}\n"
                
                if not rsi.empty:
                    response += f"14-day RSI: {rsi.iloc[0]['RSI']:.2f}\n"
                
                # Add some basic statistics
                response += f"\nPrice Statistics:\n"
                response += f"Highest Price (20 days): ${data['2. high'].max():.2f}\n"
                response += f"Lowest Price (20 days): ${data['3. low'].min():.2f}\n"
                response += f"Average Volume: {data['5. volume'].mean():,.0f}\n"
            
            return response
            
        except Exception as e:
            return f"Error fetching data for {symbol} from Alpha Vantage: {str(e)}"

class MultiProviderFinancialData:
    """
    Multi-provider system with fallbacks
    Only includes providers that are actually usable (have API keys or don't require them)
    """
    
    def __init__(self):
        self.providers = []
        
        # Always include Yahoo Finance (no API key required)
        self.providers.append(YahooFinanceProvider())
        
        # Only include Polygon if API key is available
        polygon_key = os.getenv('POLYGON_API_KEY', '')
        if polygon_key:
            self.providers.append(PolygonProvider())
        
        # Only include Finnhub if API key is available  
        finnhub_key = os.getenv('FINNHUB_API_KEY', '')
        if finnhub_key:
            self.providers.append(FinnhubProvider())
        
        # Always include Alpha Vantage (has demo key fallback)
        if ALPHA_VANTAGE_AVAILABLE:
            try:
                self.providers.append(AlphaVantageProvider())
            except ImportError as e:
                print(f"Warning: Alpha Vantage provider not available: {e}")
        
        # Note: Mock data provider removed from production
        # It's available in simple_fallback_provider.py for testing only
    
    def get_financial_data(self, symbol: str) -> str:
        """
        Try providers in order until one succeeds
        """
        last_error = ""
        
        for i, provider in enumerate(self.providers):
            try:
                print(f"🔄 Trying provider {i+1}/{len(self.providers)}: {provider.name}")
                result = provider.get_financial_data(symbol)
                
                if not result.startswith("Error:") and not result.startswith("All providers failed"):
                    print(f"✅ Success with {provider.name}")
                    return result
                    
                print(f"❌ {provider.name} failed: {result[:100]}...")
                last_error = result
                
                # Small delay between providers to avoid rate limiting
                if i < len(self.providers) - 1:  # Don't delay after last provider
                    time.sleep(0.5)
                    
            except Exception as e:
                error_msg = f"Error with {provider.name}: {str(e)}"
                print(f"❌ {error_msg}")
                last_error = error_msg
                continue
        
        # All real providers failed - return helpful error message
        provider_names = [provider.name for provider in self.providers]
        return f"""Error: All financial data providers failed.

Attempted providers: {', '.join(provider_names)}
Last error: {last_error}

Possible solutions:
1. Check your internet connection
2. Try again later (Yahoo Finance may be temporarily down)
3. Add API keys for additional providers in your .env file:
   - POLYGON_API_KEY (5 calls/minute)
   - FINNHUB_API_KEY (60 calls/minute) 
   - ALPHA_VANTAGE_API_KEY (25 calls/day)

Note: This system never returns fake/mock data in production."""
    
    def get_active_provider_count(self) -> int:
        """Get count of active providers"""
        return len(self.providers)
    
    def get_active_provider_names(self) -> list:
        """Get list of active provider names"""
        return [provider.name for provider in self.providers]
    
    def get_provider_status(self) -> str:
        """
        Get status of all providers (active and excluded)
        """
        status = "📊 Financial Data Provider Status:\n"
        status += "=" * 50 + "\n\n"
        
        status += "✅ ACTIVE PROVIDERS:\n"
        for i, provider in enumerate(self.providers, 1):
            status += f"{i}. {provider.name}\n"
            status += f"   Rate Limit: {provider.rate_limit}\n"
            if hasattr(provider, 'api_key'):
                status += f"   API Key: ✅ Configured\n"
            else:
                status += f"   API Key: ✅ Not required\n"
            status += "\n"
        
        # Show excluded providers
        excluded = []
        polygon_key = os.getenv('POLYGON_API_KEY', '')
        finnhub_key = os.getenv('FINNHUB_API_KEY', '')
        alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY', '')
        
        if not polygon_key:
            excluded.append("Polygon.io (No API key)")
        if not finnhub_key:
            excluded.append("Finnhub (No API key)")
        if not ALPHA_VANTAGE_AVAILABLE:
            excluded.append("Alpha Vantage (Library not installed)")
        
        if excluded:
            status += "⚠️  EXCLUDED PROVIDERS:\n"
            for provider in excluded:
                status += f"   • {provider}\n"
            status += "\n"
            status += "💡 To enable more providers, add API keys to your .env file\n"
            status += "   See .env-example for required variable names\n"
        else:
            status += "🎉 All providers with API keys are active!\n"
        
        status += "\n📋 IMPORTANT: This system only provides real financial data.\n"
        status += "   No mock/fake data is ever returned in production mode.\n"
        
        return status 