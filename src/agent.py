from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor, Tool
from langchain.prompts import StringPromptTemplate, PromptTemplate
from langchain_community.llms import Ollama
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import format_tool_to_openai_function
from typing import List, Union
import os
from dotenv import load_dotenv
from pydantic import Field

# Load environment variables
load_dotenv()

# Define some example tools
def search_tool(query: str) -> str:
    """Search for information about a topic."""
    return f"Searching for: {query}"

def calculator_tool(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

# Create tools
tools = [
    Tool(
        name="Search",
        func=search_tool,
        description="Useful for searching for information about a topic"
    ),
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for performing mathematical calculations"
    )
]

# Create the LLM using Ollama with Mistral model
llm = Ollama(
    model="mistral",
    temperature=0.7,
    base_url="http://localhost:11434"
)

# Create the prompt template
prompt = PromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tools:

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

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
)

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True
)

def main():
    print("Local AI Agent is ready! Type 'exit' to quit.")
    print("Note: Make sure Ollama is running with the Mistral model installed.")
    while True:
        user_input = input("\nYour question: ")
        if user_input.lower() == 'exit':
            break
        try:
            response = agent_executor.invoke({"input": user_input})
            print(f"\nFinal Answer: {response['output']}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 