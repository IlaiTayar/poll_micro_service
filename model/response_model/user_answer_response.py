from typing import Dict

from pydantic import BaseModel

from model.base_model.statistics import AnswerEntry


class UserAnswerResponse(BaseModel):
    user_id: int
    question_answer: Dict[int, AnswerEntry]
