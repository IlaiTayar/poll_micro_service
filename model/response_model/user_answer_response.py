from typing import Optional

from model.base_model.answer_option import AnswerOption
from pydantic import BaseModel


class UserAnswerResponse(BaseModel):
    user_id: int
    question_answer: dict[int, dict]
