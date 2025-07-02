"""
Test-only provider system that includes mock data for testing
This should NEVER be used in production!
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_data_providers import MultiProviderFinancialData, YahooFinanceProvider, PolygonProvider, FinnhubProvider, AlphaVantageProvider
from simple_fallback_provider import SimpleFallbackProvider
import os

class TestMultiProviderFinancialData(MultiProviderFinancialData):
    """
    Test version of MultiProviderFinancialData that includes mock data
    ⚠️  WARNING: ONLY FOR TESTING - NEVER USE IN PRODUCTION!
    """
    
    def __init__(self):
        # Initialize empty providers list
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
        try:
            self.providers.append(AlphaVantageProvider())
        except ImportError as e:
            print(f"Warning: Alpha Vantage provider not available: {e}")
        
        # ⚠️  TESTING ONLY: Include mock data provider
        self.providers.append(SimpleFallbackProvider())
    
    def get_provider_status(self) -> str:
        """
        Get status for test system (includes warning about mock data)
        """
        status = "🧪 TEST FINANCIAL DATA PROVIDER STATUS:\n"
        status += "=" * 50 + "\n"
        status += "⚠️  WARNING: THIS IS THE TEST SYSTEM!\n"
        status += "   Mock data may be returned for testing purposes.\n"
        status += "   DO NOT USE FOR REAL FINANCIAL DECISIONS!\n\n"
        
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
        # Alpha Vantage is always available (has demo key)
        
        if excluded:
            status += "⚠️  EXCLUDED PROVIDERS:\n"
            for provider in excluded:
                status += f"   • {provider}\n"
            status += "\n"
        
        return status 