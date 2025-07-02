from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from financial_agents import FinancialAnalysisAgent
from langchain_community.llms import Ollama

# Load environment variables
load_dotenv()

app = FastAPI(title="Interactive Financial Analysis System")

# Get the directory paths relative to project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
static_dir = os.path.join(project_root, "static")
templates_dir = os.path.join(project_root, "templates")

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates = Jinja2Templates(directory=templates_dir)

# Initialize the LLM and agent
llm = Ollama(
    model="llama3.1:8b",
    temperature=0.7,
    base_url="http://localhost:11434"
)

# Initialize the financial analysis agent
financial_agent = FinancialAnalysisAgent(llm)

# Pydantic models for request validation
class ConversationRequest(BaseModel):
    company_name: str
    message: str
    history: list

class FeedbackRequest(BaseModel):
    company_name: str
    feedback: str
    history: list

class CritiqueRequest(BaseModel):
    company_name: str
    history: list

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_company(company_name: str = Form(...)):
    """Initial analysis endpoint"""
    try:
        # Get financial data
        financial_data = financial_agent.get_financial_data(company_name)
        
        # Create analysis prompt
        analysis_prompt = f"""Based on the following financial data for {company_name}, provide a comprehensive investment analysis:

{financial_data}

Please provide:
1. Key financial metrics summary
2. Technical analysis insights
3. Investment recommendation for 3-5 year horizon
4. Risk assessment
5. Key factors to watch

Be thorough but concise in your analysis."""

        # Get analysis from LLM
        analysis = llm.invoke(analysis_prompt)
        
        return JSONResponse({
            "status": "success",
            "data": {
                "final_analysis": analysis,
                "history": [
                    {"type": "analysis", "content": analysis}
                ]
            }
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

@app.post("/conversation")
async def handle_conversation(request: ConversationRequest):
    """Handle ongoing conversation with the model"""
    try:
        # Create conversation context
        context = f"""You are a financial analyst having a conversation about {request.company_name}. 
        
Previous conversation context:
"""
        
        # Add conversation history
        for msg in request.history[-6:]:  # Keep last 6 messages for context
            if msg['role'] == 'user':
                context += f"User: {msg['content']}\n"
            else:
                context += f"Assistant: {msg['content']}\n"
        
        context += f"\nUser's current message: {request.message}\n\n"
        context += "Please provide a helpful response that continues the conversation and addresses the user's input."
        
        # Get response from LLM
        response = llm.invoke(context)
        
        return JSONResponse({
            "status": "success",
            "response": response
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

@app.post("/feedback")
async def handle_feedback(request: FeedbackRequest):
    """Handle user feedback and provide improved analysis"""
    try:
        # Create feedback prompt
        feedback_prompt = f"""You are a financial analyst. The user has provided feedback on your analysis of {request.company_name}.

User Feedback: {request.feedback}

Previous analysis context:
"""
        
        # Add recent conversation history
        for msg in request.history[-4:]:
            if msg['role'] == 'assistant':
                feedback_prompt += f"Previous Analysis: {msg['content']}\n"
        
        feedback_prompt += f"""
Based on the user's feedback, please provide an improved or additional analysis that addresses their specific request.

Focus on:
- Addressing the specific feedback provided
- Providing more detailed or targeted analysis
- Incorporating the user's guidance into your recommendations

Please be specific and actionable in your response."""

        # Get improved analysis from LLM
        response = llm.invoke(feedback_prompt)
        
        return JSONResponse({
            "status": "success",
            "response": response
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

@app.post("/critique")
async def run_critique_analysis(request: CritiqueRequest):
    """Run critique analysis on the current analysis"""
    try:
        # Find the most recent analysis in conversation history
        recent_analysis = None
        for msg in reversed(request.history):
            if msg['role'] == 'assistant' and 'analysis' in msg['content'].lower():
                recent_analysis = msg['content']
                break
        
        if not recent_analysis:
            # If no analysis found, get fresh financial data and create analysis
            financial_data = financial_agent.get_financial_data(request.company_name)
            analysis_prompt = f"""Based on the following financial data for {request.company_name}, provide a comprehensive investment analysis:

{financial_data}

Please provide:
1. Key financial metrics summary
2. Technical analysis insights
3. Investment recommendation for 3-5 year horizon
4. Risk assessment
5. Key factors to watch

Be thorough but concise in your analysis."""
            recent_analysis = llm.invoke(analysis_prompt)
        
        # Create critique prompt
        critique_prompt = f"""You are a critical financial analyst. Review the following analysis and identify potential flaws, biases, or areas for improvement.

Analysis to Critique:
{recent_analysis}

Provide your critique in the following format:
1. Identified Issues
2. Potential Biases
3. Missing Information
4. Alternative Perspectives
5. Recommendations for Improvement

Be concise and prescriptive in your criticism. Focus on actionable improvements."""
        
        # Get critique from LLM
        critique = llm.invoke(critique_prompt)
        
        # Optionally generate improved analysis based on critique
        improved_prompt = f"""Based on the following critique of the analysis for {request.company_name}, provide an improved analysis that addresses the identified issues:

Original Analysis:
{recent_analysis}

Critique:
{critique}

Please provide an improved analysis that:
1. Addresses the specific issues identified in the critique
2. Incorporates the alternative perspectives mentioned
3. Includes the missing information highlighted
4. Provides more balanced and comprehensive recommendations

Make the analysis more robust and actionable based on the critique feedback."""
        
        improved_analysis = llm.invoke(improved_prompt)
        
        return JSONResponse({
            "status": "success",
            "critique": critique,
            "improved_analysis": improved_analysis
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

@app.get("/cache-status")
async def get_cache_status():
    """Get cache status information"""
    try:
        cache_status = financial_agent.get_cache_status()
        return JSONResponse({
            "status": "success",
            "status_text": cache_status
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 