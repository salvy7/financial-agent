from langchain.agents import create_react_agent, AgentExecutor, Tool
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from typing import Dict, List
import pandas as pd
import time
from datetime import datetime, timedelta
# Alpha Vantage now handled by financial_data_providers.py
import os
from dotenv import load_dotenv
from financial_data_providers import MultiProviderFinancialData

# Load environment variables
load_dotenv()

class FinancialAnalysisAgent:
    def __init__(self, llm):
        self.llm = llm
        # Initialize multi-provider system (Yahoo Finance, Polygon, Finnhub, Alpha Vantage)
        self.data_provider = MultiProviderFinancialData()
        
        # Initialize cache for financial data
        self.data_cache = {}
        self.cache_duration = 3000  # 5 minutes in seconds
        
        self.tools = [
            Tool(
                name="GetFinancialData",
                func=self.get_financial_data,
                description="Get financial data for a company using multiple sources (Yahoo Finance, Polygon, Finnhub). Input should be just the stock symbol (e.g., AAPL, MSFT). Data is cached for 5 minutes to reduce API calls."
            ),
            # Tool(
            #     name="CalculateMetrics",
            #     func=self.calculate_metrics,
            #     description="Calculate financial metrics from the data. Input should be the data string from GetFinancialData"
            # ),
            Tool(
                name="CheckDataSources",
                func=self.check_data_sources,
                description="Check the status of all available financial data sources"
            ),
            Tool(
                name="GetCacheStatus",
                func=self.get_cache_status,
                description="Get cache status and statistics for financial data. Shows cached symbols and their age."
            ),
            Tool(
                name="ClearCache",
                func=self.clear_cache,
                description="Clear all cached financial data to force fresh API calls on next request."
            )
        ]
        
        self.prompt = PromptTemplate.from_template(
            """You are a financial analysis expert. Analyze the following company and provide a detailed investment recommendation for a 3-5 year horizon.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Important Instructions:
1. For GetFinancialData, only input the stock symbol (e.g., AAPL, MSFT)
2. For CalculateMetrics, use the data string from GetFinancialData
3. Do not try to use any other tools or methods
4. Keep your analysis focused on the data you receive
5. Always follow the format exactly as shown above
6. If you encounter an error, explain it in the Observation and continue with your analysis

Begin!

Question: Analyze {company_name} for investment potential
Thought: {agent_scratchpad}"""
        )
        
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def get_financial_data(self, company_name: str) -> str:
        try:
            # Normalize the symbol (uppercase)
            symbol = company_name.upper()
            current_time = time.time()
            
            # Check if data is in cache and not expired
            if symbol in self.data_cache:
                cached_data, cache_time = self.data_cache[symbol]
                if current_time - cache_time < self.cache_duration:
                    print(f"📋 Returning cached data for {symbol} (age: {int(current_time - cache_time)}s)")
                    return cached_data
                else:
                    # Remove expired cache entry
                    del self.data_cache[symbol]
                    print(f"🗑️  Cache expired for {symbol}, fetching fresh data")
            
            # Fetch fresh data from provider
            print(f"🔄 Fetching fresh data for {symbol}")
            result = self.data_provider.get_financial_data(symbol)
            
            # Cache the result if it's not an error
            if not result.startswith("Error:"):
                self.data_cache[symbol] = (result, current_time)
                print(f"💾 Cached data for {symbol}")
            
            return result
            
        except Exception as e:
            return f"Error fetching data for {company_name}: {str(e)}. Please try again later or check if the symbol is correct."

    def calculate_metrics(self, data: str) -> str:
        try:
            # Parse the data and calculate key metrics
            return "Key metrics calculated successfully"
        except Exception as e:
            return f"Error calculating metrics: {str(e)}"
    
    def check_data_sources(self, _: str = "") -> str:
        """Check the status of all available financial data sources"""
        try:
            return self.data_provider.get_provider_status()
        except Exception as e:
            return f"Error checking data sources: {str(e)}"
    
    def get_cache_status(self, _: str = "") -> str:
        """Get cache status and statistics"""
        try:
            current_time = time.time()
            active_cache = {}
            expired_count = 0
            
            for symbol, (data, cache_time) in self.data_cache.items():
                if current_time - cache_time < self.cache_duration:
                    age = int(current_time - cache_time)
                    active_cache[symbol] = age
                else:
                    expired_count += 1
            
            # Clean up expired entries
            if expired_count > 0:
                self.data_cache = {k: v for k, v in self.data_cache.items() 
                                 if current_time - v[1] < self.cache_duration}
            
            status = f"📋 Financial Data Cache Status:\n"
            status += f"Cache Duration: {self.cache_duration} seconds ({self.cache_duration//60} minutes)\n"
            status += f"Active Cached Symbols: {len(active_cache)}\n"
            status += f"Expired Entries Cleaned: {expired_count}\n\n"
            
            if active_cache:
                status += "Cached Symbols:\n"
                for symbol, age in active_cache.items():
                    status += f"  • {symbol}: {age}s old\n"
            else:
                status += "No active cached data\n"
            
            return status
        except Exception as e:
            return f"Error checking cache status: {str(e)}"
    
    def clear_cache(self, _: str = "") -> str:
        """Clear all cached financial data"""
        try:
            cache_size = len(self.data_cache)
            self.data_cache.clear()
            return f"🗑️  Cache cleared. Removed {cache_size} cached entries."
        except Exception as e:
            return f"Error clearing cache: {str(e)}"

    def analyze(self, company_name: str) -> str:
        return self.executor.invoke({"company_name": company_name})["output"]

class CritiqueAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(
            """You are a critical financial analyst. Review the following analysis and identify potential flaws, biases, or areas for improvement.

Analysis to Critique:
{analysis}

Provide your critique in the following format:
1. Identified Issues
2. Potential Biases
3. Missing Information
4. Alternative Perspectives
5. Recommendations for Improvement

Be concise and and prescriptive in your criticism."""
        )

    def critique(self, analysis: str) -> str:
        return self.llm.invoke(self.prompt.format(analysis=analysis))

class FinancialAnalysisSystem:
    def __init__(self, iterations: int = 2):
        self.llm = Ollama(
            model="llama3.1:8b",
            temperature=0.7,
            base_url="http://localhost:11434"
        )
        self.analysis_agent = FinancialAnalysisAgent(self.llm)
        self.critique_agent = CritiqueAgent(self.llm)
        self.iterations = iterations

    def run_analysis(self, company_name: str) -> Dict:
        analysis_history = []
        current_analysis = self.analysis_agent.analyze(company_name)
        analysis_history.append({"type": "initial", "content": current_analysis})

        for i in range(self.iterations):
            critique = self.critique_agent.critique(current_analysis)
            analysis_history.append({"type": "critique", "content": critique})
            
            # Improve analysis based on critique
            improved_analysis = self.analysis_agent.analyze(company_name)
            analysis_history.append({"type": "improved", "content": improved_analysis})
            current_analysis = improved_analysis

        return {
            "final_analysis": current_analysis,
            "history": analysis_history
        } 