from pydantic import BaseModel


class QuestionRequest(BaseModel):
    poll_id: int
    question_text: str