from typing import List

from pydantic import BaseModel

from model.base_model.answer_option import AnswerOption


class QuestionResponse(BaseModel):
    question_id: int
    question_text: str
    options: List[AnswerOption]