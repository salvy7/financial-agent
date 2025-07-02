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

### **Multi-Provider Data System**
The system automatically tries data sources in this order:
1. **Yahoo Finance** (Primary) - Unlimited requests, rich data
2. **Polygon.io** (Backup) - If Yahoo fails and API key provided
3. **Finnhub** (Backup) - If others fail and API key provided  
4. **Alpha Vantage** (Final fallback) - If all else fails

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

### **Rate Limits Comparison**
| Provider | Free Tier Limit | Data Quality | API Key Required |
|----------|----------------|--------------|------------------|
| Yahoo Finance | ~Unlimited | ⭐⭐⭐⭐⭐ | ❌ No |
| Polygon.io | 5/minute | ⭐⭐⭐⭐ | ✅ Yes |
| Finnhub | 60/minute | ⭐⭐⭐⭐ | ✅ Yes |
| Alpha Vantage | 25/day, 5/min | ⭐⭐⭐ | ✅ Yes |

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

### **Dramatically Better Rate Limits**
- **Before**: Limited to 25 requests/day with Alpha Vantage
- **Now**: Virtually unlimited with Yahoo Finance primary source
- **Reliability**: Automatic fallbacks ensure high availability
- **No Setup Required**: Works immediately without any API keys

### **Enhanced Data Quality**
- Company fundamentals (P/E ratio, market cap, dividend yield)
- Multiple timeframe analysis (1 week, 1 month, 1 year performance)
- Advanced technical indicators (20-day SMA, 50-day SMA, RSI)
- Real-time pricing with comprehensive historical data

This system gives you **enterprise-grade financial data access** for free! 🚀

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
- ✅ Multi-provider fallback system
- ✅ Mock data provider functionality
- ✅ Error handling and rate limit management 