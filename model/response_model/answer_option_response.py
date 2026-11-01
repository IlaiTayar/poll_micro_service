from pydantic import BaseModel


class AnswerOptionResponse(BaseModel):
    option_id: int
    option_text: str