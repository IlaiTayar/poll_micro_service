from pydantic import BaseModel


class AnswerOptionRequest(BaseModel):
    question_id: int
    option_text: str