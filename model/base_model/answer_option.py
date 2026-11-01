from typing import Optional

from pydantic import BaseModel


class AnswerOption(BaseModel):
    option_id: int
    question_id: int
    option_text: str
