from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Question(BaseModel):
    question_id: Optional[int] = None
    poll_id: int
    question_text: str