from typing import List

from pydantic import BaseModel

from model.response_model.answer_option_response import AnswerOptionResponse


class QuestionResponse(BaseModel):
    question_id: int
    question_text: str
    options: List[AnswerOptionResponse]