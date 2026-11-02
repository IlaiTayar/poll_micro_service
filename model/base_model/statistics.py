from typing import Any, Dict, Optional

from pydantic import BaseModel


class QuestionOptionStat(BaseModel):
    question_id: int
    option_id: int
    option_text: str
    count: int


class QuestionTotalStat(BaseModel):
    question_id: int
    total_users_answered: int


class AnswerEntry(BaseModel):
    answer_id: int
    question_id: int
    question_text: str
    option_id: Optional[int] = None
    option_text: Optional[str] = None


class UserAnswerSummaryEntry(BaseModel):
    answer_id: int
    user_id: int
    question_id: int
    question_text: Optional[str] = None
    option_id: Optional[int] = None
    option_text: Optional[str] = None


class UserAnswerSummary(BaseModel):
    user_id: int
    question_answer: Dict[int, AnswerEntry]


class UserTotalAnsweredStat(BaseModel):
    user_id: int
    total_questions_answered: int


class QuestionResultsEntry(BaseModel):
    poll_id: int
    question_id: int
    question_text: str
    option_id: Optional[int] = None
    option_text: Optional[str] = None
    count: int
