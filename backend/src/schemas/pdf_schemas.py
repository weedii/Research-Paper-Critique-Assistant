from pydantic import BaseModel
from typing import List, Optional


class PaperSection(BaseModel):
    """Schema for each extracted section of a research paper"""

    goal: Optional[str] = None
    hypothesis: Optional[str] = None
    methods: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None


class PaperCritique(BaseModel):
    """Schema for the critique of a research paper"""

    critique: str


class ReviewerQuestions(BaseModel):
    """Schema for suggested reviewer questions"""

    questions: List[str]


class PaperAnalysisResponse(BaseModel):
    """Schema for the full analysis response"""

    goal: Optional[str] = None
    hypothesis: Optional[str] = None
    methods: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None
    critique: Optional[str] = None
    reviewer_questions: Optional[List[str]] = None
