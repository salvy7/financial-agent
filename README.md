# Financial Analysis System

A comprehensive financial analysis system using AI agents that provides investment recommendations through iterative analysis and self-critique.

## Project Structure

```
├── src/                              # Source code
│   ├── __init__.py
│   ├── financial_agents.py           # Main financial analysis agents
│   ├── financial_data_providers.py   # Multi-provider data system
│   ├── simple_fallback_provider.py   # Mock data fallback provider
│   ├── app.py                        # FastAPI web application
│   └── agent.py                      # Command-line agent
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── test_providers.py             # Multi-provider system tests
│   └── debug_yfinance.py             # Yahoo Finance debugging tools
├── static/                           # Static web assets
├── templates/                        # HTML templates
├── main.py                           # Web application entry point
├── cli.py                            # Command-line interface entry point
├── run_tests.py                      # Test runner script
├── .env-example                      # Environment variables template
├── requirements.txt                  # Python dependencies
└── README.md
```

## Features

- **Multi-Agent Architecture**: Financial analysis and critique agents working together
- **Multiple Data Sources**: Yahoo Finance (primary), Polygon.io, Finnhub, Alpha Vantage (fallback)
- **High Rate Limits**: Yahoo Finance provides virtually unlimited requests vs Alpha Vantage's 25/day
- **Rich Financial Data**: Real-time quotes, historical data, technical indicators, fundamentals
- **Technical Analysis**: RSI, SMA, price trends, and comprehensive market analysis
- **Iterative Improvement**: Self-critiquing system that improves analysis over multiple iterations
- **Web & CLI Interfaces**: Both web UI and command-line interfaces available
- **Local AI**: Runs completely locally using Ollama with Mistral model
- **Automatic Fallbacks**: If one data source fails, automatically tries the next

## Prerequisites

1. **Install Ollama** from https://ollama.ai/
2. **Pull the Mistral model:**
   ```bash
   ollama pull mistral
   ```
3. **API Keys (Optional):**
   - **Yahoo Finance**: No API key required ✅ (Primary source)
   - **Polygon.io**: Free 5 calls/minute - https://polygon.io/
   - **Finnhub**: Free 60 calls/minute - https://finnhub.io/
   - **Alpha Vantage**: Free 25 calls/day - https://www.alphavantage.co/support/#api-key

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file** (optional - copy from `.env-example`):
   ```env
   # Only add the API keys you want to use (Yahoo Finance works without any keys)
   POLYGON_API_KEY=your_polygon_key_here
   FINNHUB_API_KEY=your_finnhub_key_here  
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
   ```

3. **Start Ollama server:**
   ```bash
   ollama serve
   ```

## Running the Application

### Web Interface (Recommended)
```bash
python main.py
```
Access the web interface at: http://localhost:8000

### Command Line Interface
```bash
python cli.py
```

### Direct Python Usage
```python
import sys
sys.path.append('src')
from financial_agents import FinancialAnalysisSystem

# Initialize and run analysis
system = FinancialAnalysisSystem(iterations=2)
result = system.run_analysis("AAPL")
print(result["final_analysis"])
```

## How It Works

### **Smart Multi-Provider Data System**
The system intelligently includes only usable providers:

**Default Setup (No API Keys Needed):**
1. **Yahoo Finance** (Primary) - Unlimited requests, rich data
2. **Alpha Vantage** (Fallback) - Demo key available, 25 calls/day with API key
3. **Graceful Error Handling** - Clear error messages if all providers fail

**With Optional API Keys:**
- **Polygon.io** - Added if `POLYGON_API_KEY` is configured (5 calls/min)
- **Finnhub** - Added if `FINNHUB_API_KEY` is configured (60 calls/min)
- **Alpha Vantage** - Added if `ALPHA_VANTAGE_API_KEY` is configured (25 calls/day)

### **AI Agent Architecture**
1. **FinancialAnalysisAgent**: 
   - Fetches real-time financial data from multiple sources
   - Performs technical analysis (RSI, SMA, price trends, fundamentals)
   - Generates initial investment recommendations

2. **CritiqueAgent**: 
   - Reviews the analysis for biases and flaws
   - Identifies missing information
   - Suggests improvements

3. **FinancialAnalysisSystem**: 
   - Orchestrates multiple iterations of analysis and critique
   - Produces refined investment recommendations

### **Provider Comparison**

**🚀 Default Providers (Always Active):**
| Provider | Rate Limit | Data Quality | Setup Required |
|----------|------------|--------------|----------------|
| Yahoo Finance | ~Unlimited | ⭐⭐⭐⭐⭐ | ❌ None |
| Alpha Vantage | Demo key (limited) | ⭐⭐⭐ | ❌ None |

**⚙️ Optional Providers (API Key Required):**
| Provider | Rate Limit | Data Quality | Setup |
|----------|------------|--------------|-------|
| Polygon.io | 5/minute | ⭐⭐⭐⭐ | Add `POLYGON_API_KEY` |
| Finnhub | 60/minute | ⭐⭐⭐⭐ | Add `FINNHUB_API_KEY` |
| Alpha Vantage | 25/day | ⭐⭐⭐ | Add `ALPHA_VANTAGE_API_KEY` (enhances demo key) |

## Usage Examples

### Stock Symbols to Try:
- `AAPL` - Apple Inc.
- `MSFT` - Microsoft
- `GOOGL` - Alphabet/Google
- `TSLA` - Tesla
- `NVDA` - NVIDIA
- `META` - Meta Platforms

### Sample Analysis Output:
The system provides comprehensive analysis including:
- Current stock price and volume data
- Technical indicators (20-day SMA, 14-day RSI)
- Price trends and statistics
- Investment recommendation for 3-5 year horizon
- Risk assessment and alternative perspectives

## Troubleshooting

- **"Connection refused"**: Ensure Ollama is running (`ollama serve`)
- **"API rate limit"**: Very rare with Yahoo Finance primary source
- **"No data available"**: Verify the stock symbol is correct (try with and without exchange suffix)
- **"All providers failed"**: Check internet connection; Yahoo Finance should always work
- **Import errors**: Make sure you're running from the project root directory
- **Slow responses**: Normal on first request; Yahoo Finance caches data effectively

## Customization

- **Adjust iterations**: Change the `iterations` parameter in `FinancialAnalysisSystem`
- **Add more tools**: Extend the agent's capabilities in `financial_agents.py`
- **Modify prompts**: Customize analysis prompts for different investment strategies
- **Change AI model**: Switch to different Ollama models (e.g., `llama2`, `codellama`)

## Benefits of Multi-Provider System

### **Dramatically Better Experience**
- **Before**: Limited to 25 requests/day with Alpha Vantage
- **Now**: Virtually unlimited with Yahoo Finance + instant setup
- **Smart Providers**: Only uses providers that actually work (no wasted attempts)
- **Zero Setup**: Works immediately - just run and go!
- **Optional Scaling**: Add API keys only if you want additional providers

### **Enhanced Data Quality**
- Company fundamentals (P/E ratio, market cap, dividend yield)
- Multiple timeframe analysis (1 week, 1 month, 1 year performance)
- Advanced technical indicators (20-day SMA, 50-day SMA, RSI)
- Real-time pricing with comprehensive historical data

This system gives you **enterprise-grade financial data access** for free! 🚀

### **Production Safety & Error Handling**
- **Real Data Only**: Never returns fake/mock data in production
- **Clear Error Messages**: If all providers fail, you get helpful error messages (not fake data)
- **Test Support**: Mock data available in `test_provider_system.py` for development only
- **Transparent Failures**: Always know when you're getting real vs unavailable data

## Testing

### **Run All Tests**
```bash
python run_tests.py
```

### **Run Specific Tests**
```bash
python run_tests.py providers    # Test multi-provider system
python run_tests.py debug        # Debug Yahoo Finance issues
```

### **Manual Testing**
```bash
# Test individual providers
cd tests
python test_providers.py

# Debug specific issues
python debug_yfinance.py
```

The test suite verifies:
- ✅ Yahoo Finance integration (fast_info and historical data)
- ✅ Multi-provider fallback system (with test-only mock data)
- ✅ Production system excludes mock data (safety check)
- ✅ Error handling and rate limit management

**Note**: Tests use `tests/test_provider_system.py` and `tests/simple_fallback_provider.py` which include mock data for reliable testing. The production system (`src/financial_data_providers.py`) never includes mock data. 