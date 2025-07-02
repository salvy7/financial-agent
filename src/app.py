from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from financial_agents import FinancialAnalysisSystem

# Load environment variables
load_dotenv()

app = FastAPI(title="Financial Analysis System")

# Get the directory paths relative to project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
static_dir = os.path.join(project_root, "static")
templates_dir = os.path.join(project_root, "templates")

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates = Jinja2Templates(directory=templates_dir)

# Initialize the financial analysis system
financial_system = FinancialAnalysisSystem(iterations=2)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_company(company_name: str = Form(...)):
    try:
        result = financial_system.run_analysis(company_name)
        return JSONResponse({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 