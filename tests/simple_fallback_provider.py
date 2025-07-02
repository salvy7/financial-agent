"""
Simple fallback provider that creates mock data for testing
"""

import time
from datetime import datetime

class SimpleFallbackProvider:
    """
    Simple fallback provider that creates realistic mock data for testing
    """
    
    def __init__(self):
        self.name = "Mock Data Provider"
        self.rate_limit = "Unlimited (for testing)"
    
    def get_financial_data(self, symbol: str) -> str:
        """
        Generate mock but realistic financial data for testing
        """
        try:
            # Mock data based on common stocks
            mock_data = {
                'AAPL': {
                    'name': 'Apple Inc.',
                    'sector': 'Technology',
                    'price': 185.50,
                    'high': 188.20,
                    'low': 183.90,
                    'volume': 45000000,
                    'market_cap': 2900000000000,
                    'pe_ratio': 28.5,
                    'dividend_yield': 0.005
                },
                'MSFT': {
                    'name': 'Microsoft Corporation',
                    'sector': 'Technology',
                    'price': 375.80,
                    'high': 378.50,
                    'low': 372.10,
                    'volume': 32000000,
                    'market_cap': 2800000000000,
                    'pe_ratio': 32.1,
                    'dividend_yield': 0.0067
                },
                'GOOGL': {
                    'name': 'Alphabet Inc.',
                    'sector': 'Technology',
                    'price': 142.30,
                    'high': 145.20,
                    'low': 140.80,
                    'volume': 28000000,
                    'market_cap': 1800000000000,
                    'pe_ratio': 25.8,
                    'dividend_yield': 0.0
                },
                'TSLA': {
                    'name': 'Tesla Inc.',
                    'sector': 'Automotive',
                    'price': 248.90,
                    'high': 252.70,
                    'low': 245.30,
                    'volume': 85000000,
                    'market_cap': 780000000000,
                    'pe_ratio': 62.5,
                    'dividend_yield': 0.0
                }
            }
            
            # Use mock data if available, otherwise generate generic data
            if symbol.upper() in mock_data:
                data = mock_data[symbol.upper()]
            else:
                # Generate generic mock data
                data = {
                    'name': f'{symbol} Corporation',
                    'sector': 'Unknown',
                    'price': 100.00,
                    'high': 102.50,
                    'low': 98.75,
                    'volume': 1000000,
                    'market_cap': 50000000000,
                    'pe_ratio': 20.0,
                    'dividend_yield': 0.02
                }
            
            # Format response
            response = f"Financial Data for {symbol} ({data['name']}):\n"
            response += f"Data Source: {self.name} (MOCK DATA - FOR TESTING ONLY)\n"
            response += f"Sector: {data['sector']}\n\n"
            
            response += f"Latest Trading Data ({datetime.now().strftime('%Y-%m-%d')}):\n"
            response += f"Current Price: ${data['price']:.2f}\n"
            response += f"Day High: ${data['high']:.2f}\n"
            response += f"Day Low: ${data['low']:.2f}\n"
            response += f"Volume: {data['volume']:,}\n"
            
            # Calculate mock change
            prev_close = data['price'] * 0.995  # Mock -0.5% from previous
            change_pct = ((data['price'] - prev_close) / prev_close) * 100
            response += f"Previous Close: ${prev_close:.2f}\n"
            response += f"Change: {change_pct:.2f}%\n"
            
            response += f"\nFundamental Data:\n"
            response += f"Market Cap: ${data['market_cap']:,.0f}\n"
            response += f"P/E Ratio: {data['pe_ratio']:.2f}\n"
            if data['dividend_yield'] > 0:
                response += f"Dividend Yield: {data['dividend_yield']*100:.2f}%\n"
            
            response += f"\n⚠️  NOTE: This is MOCK DATA for testing purposes only.\n"
            response += f"Real financial data providers are currently unavailable.\n"
            
            return response
            
        except Exception as e:
            return f"Error in fallback provider: {str(e)}" 