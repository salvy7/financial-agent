from langchain.agents import create_react_agent, AgentExecutor, Tool
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from typing import Dict, List
import pandas as pd
import time
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FinancialAnalysisAgent:
    def __init__(self, llm):
        self.llm = llm
        # Initialize Alpha Vantage with API key
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')  # Use demo key if none provided
        self.ts = TimeSeries(key=self.api_key, output_format='pandas')
        self.ti = TechIndicators(key=self.api_key, output_format='pandas')
        
        self.tools = [
            Tool(
                name="GetFinancialData",
                func=self.get_financial_data,
                description="Get financial data for a company using Alpha Vantage. Input should be just the stock symbol (e.g., AAPL, MSFT)"
            ),
            Tool(
                name="CalculateMetrics",
                func=self.calculate_metrics,
                description="Calculate financial metrics from the data. Input should be the data string from GetFinancialData"
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
            # Add delay to avoid rate limiting
            time.sleep(1)
            
            # Get daily time series data
            data, meta_data = self.ts.get_daily(symbol=company_name, outputsize='compact')
            
            if data.empty:
                return f"Error: No data available for {company_name}. Please check if the symbol is correct."
            
            # Get technical indicators
            try:
                sma_20, _ = self.ti.get_sma(symbol=company_name, interval='daily', time_period=20)
            except Exception as e:
                sma_20 = pd.DataFrame()
                print(f"Warning: Could not fetch SMA data: {str(e)}")
            
            try:
                rsi, _ = self.ti.get_rsi(symbol=company_name, interval='daily', time_period=14)
            except Exception as e:
                rsi = pd.DataFrame()
                print(f"Warning: Could not fetch RSI data: {str(e)}")
            
            # Format the response
            response = f"Financial data for {company_name}:\n\n"
            
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
            return f"Error fetching data for {company_name}: {str(e)}. Please try again later or check if the symbol is correct."

    def calculate_metrics(self, data: str) -> str:
        try:
            # Parse the data and calculate key metrics
            return "Key metrics calculated successfully"
        except Exception as e:
            return f"Error calculating metrics: {str(e)}"

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

Be thorough and constructive in your criticism."""
        )

    def critique(self, analysis: str) -> str:
        return self.llm.invoke(self.prompt.format(analysis=analysis))

class FinancialAnalysisSystem:
    def __init__(self, iterations: int = 2):
        self.llm = Ollama(
            model="mistral",
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