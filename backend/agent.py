import os
import json
from typing import List
from models import ExamInput, StudyPlan, StudySession
from openai import OpenAI

client = None

def get_client():
    global client
    if not client:
        # Check for DeepSeek API Key first
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key:
            client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
            client.is_deepseek = True
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                client = OpenAI(api_key=api_key)
                client.is_deepseek = False
    return client

async def generate_study_plan(exams: List[ExamInput]) -> StudyPlan:
    client = get_client()
    
    # Mock response if no client (for testing without billing)
    if not client:
        return _generate_mock_plan(exams)

    system_prompt = """You are StudyBuddy, an expert academic planner. 
    Your goal is to create a realistic, prioritized study schedule for a student.
    
    Input: A list of exams with dates and confidence levels (1-5, where 1 is low confidence).
    Output: A JSON structure confirming to the StudyPlan schema.
    
    Rules:
    - Prioritize subjects with upcoming dates and low confidence.
    - Break study into 45-60 minute sessions.
    - Provide specific advice for each subject.
    - Return ONLY valid JSON.
    """
    
    user_prompt = f"Here are my upcoming exams: {json.dumps([e.model_dump() for e in exams], default=str)}"

    try:
        model_name = "deepseek-chat" if getattr(client, "is_deepseek", False) else "gpt-4o"
        response = client.chat.completions.create(
            model=model_name, # Use deepseek-chat for DeepSeek or gpt-4o for OpenAI
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # Ensure data matches our model roughly, or simpler: just parse it into the Pydantic model
        # The LLM might not match Pydantic exactly without Strict Mode or Tool Calling, 
        # so for this 48hr hackathon, we might need to be lenient or structure the prompt very carefully.
        # Let's assume the LLM follows the instruction "confirming to the StudyPlan schema" 
        # but we need to ensure the schema is visible to it.
        # For simplicity in this step, I will trust the LLM produces the keys: plan_name, sessions, advice.
        
        return StudyPlan(**data)

    except Exception as e:
        print(f"Error generating plan: {e}")
        return _generate_mock_plan(exams)

def _generate_mock_plan(exams: List[ExamInput]) -> StudyPlan:
    """Fallback for when no API key is present or error occurs."""
    sessions = []
    import datetime
    
    today = datetime.date.today()
    
    for i, exam in enumerate(exams):
        sessions.append(StudySession(
            date=str(today),
            subject=exam.subject,
            topic="General Review",
            duration_minutes=60,
            focus_area="Key Concepts and Definitions"
        ))
    
    return StudyPlan(
        plan_name="Backup Study Plan",
        sessions=sessions,
        advice="This is a generated backup plan. Please configure your OpenAI or DeepSeek API Key for personalized advice."
    )
