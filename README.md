# Financial Analysis System

A comprehensive financial analysis system using AI agents that provides investment recommendations through iterative analysis and self-critique.

## Project Structure

```
├── src/                          # Source code
│   ├── __init__.py
│   ├── financial_agents.py       # Main financial analysis agents
│   ├── app.py                    # FastAPI web application
│   └── agent.py                  # Command-line agent
├── static/                       # Static web assets
├── templates/                    # HTML templates
├── main.py                       # Web application entry point
├── cli.py                        # Command-line interface entry point
├── requirements.txt              # Python dependencies
└── README.md
```

## Features

- **Multi-Agent Architecture**: Financial analysis and critique agents working together
- **Real Financial Data**: Integration with Alpha Vantage API for live market data
- **Technical Analysis**: RSI, SMA, and other technical indicators
- **Iterative Improvement**: Self-critiquing system that improves analysis over multiple iterations
- **Web & CLI Interfaces**: Both web UI and command-line interfaces available
- **Local AI**: Runs completely locally using Ollama with Mistral model

## Prerequisites

1. **Install Ollama** from https://ollama.ai/
2. **Pull the Mistral model:**
   ```bash
   ollama pull mistral
   ```
3. **Get Alpha Vantage API Key** from https://www.alphavantage.co/support/#api-key (free)

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file** in the project root:
   ```env
   ALPHA_VANTAGE_API_KEY=your_api_key_here
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

1. **FinancialAnalysisAgent**: 
   - Fetches real-time financial data from Alpha Vantage
   - Performs technical analysis (RSI, SMA, price trends)
   - Generates initial investment recommendations

2. **CritiqueAgent**: 
   - Reviews the analysis for biases and flaws
   - Identifies missing information
   - Suggests improvements

3. **FinancialAnalysisSystem**: 
   - Orchestrates multiple iterations of analysis and critique
   - Produces refined investment recommendations

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
- **"API rate limit"**: Alpha Vantage free tier has rate limits; wait between requests
- **"No data available"**: Verify the stock symbol is correct
- **Import errors**: Make sure you're running from the project root directory

## Customization

- **Adjust iterations**: Change the `iterations` parameter in `FinancialAnalysisSystem`
- **Add more tools**: Extend the agent's capabilities in `financial_agents.py`
- **Modify prompts**: Customize analysis prompts for different investment strategies
- **Change AI model**: Switch to different Ollama models (e.g., `llama2`, `codellama`)

## API Rate Limits

The system uses Alpha Vantage's free tier which has:
- 25 requests per day
- 5 API requests per minute

For production use, consider upgrading to a paid plan 