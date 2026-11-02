from typing import Optional

from pydantic import BaseModel


class Answer(BaseModel):
    user_id: int
    question_id: int
    option_id: Optional[int] = None
