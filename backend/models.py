from pydantic import BaseModel
from typing import List, Optional

class ExamInput(BaseModel):
    subject: str
    exam_date: str # YYYY-MM-DD
    confidence_level: int # 1-5

class StudyPlanRequest(BaseModel):
    exams: List[ExamInput]

class StudySession(BaseModel):
    date: str
    subject: str
    topic: str
    duration_minutes: int
    focus_area: str

class StudyPlan(BaseModel):
    plan_name: str
    sessions: List[StudySession]
    advice: str
