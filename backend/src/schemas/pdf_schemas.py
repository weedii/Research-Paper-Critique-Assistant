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
    """Schema for reviewer questions with structured format"""

    main_question: Optional[str] = None
    sub_questions: Optional[List[str]] = None
    addressed_questions: Optional[str] = None


class PaperAnalysisResponse(BaseModel):
    """Schema for the full analysis response"""

    goal: Optional[str] = None
    hypothesis: Optional[str] = None
    methods: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None
    critique: Optional[str] = None
    reviewer_questions: Optional[ReviewerQuestions] = None
