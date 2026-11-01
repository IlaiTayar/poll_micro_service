from typing import Optional

from pydantic import BaseModel

from model.base_model.answer_option import AnswerOption
from model.base_model.question import Question
from model.base_model.user_answer import UserAnswer


class UserAnswerResponse(BaseModel):
    user_id: int
    question_answer: dict[Question, Optional[AnswerOption]]