from typing import Dict, Optional

from pydantic import BaseModel


class AnswerEntry(BaseModel):
    answer_id: int
    question_id: int
    question_text: str
    option_id: Optional[int] = None
    option_text: Optional[str] = None


class UserAnswerResponse(BaseModel):
    user_id: int
    question_answer: Dict[int, AnswerEntry]
