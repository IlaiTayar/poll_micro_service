from typing import List

from pydantic import BaseModel

from model.response_model.qustion_response import QuestionResponse


class PollResponse(BaseModel):
    poll_id: int
    poll_name: str
    questions: List[QuestionResponse]