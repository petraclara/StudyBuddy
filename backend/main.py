from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import StudyPlanRequest, StudyPlan
from agent import generate_study_plan
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="StudyBuddy API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, verify this logic
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/plan", response_model=StudyPlan)
async def create_plan(request: StudyPlanRequest):
    try:
        if not os.getenv("OPENAI_API_KEY"):
             # For demo purposes if no key is present, we might want to return a mock or error
             # But let's assume the user will provide it. 
             # Falling back to mock if strictly needed can be done in agent.py
             pass
        
        plan = await generate_study_plan(request.exams)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
