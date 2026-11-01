from typing import Optional

from pydantic import BaseModel

from model.base_model.answer_option import AnswerOption


class UserAnswerResponse(BaseModel):
    user_id: int
    question_answer: dict[int, Optional[AnswerOption]]