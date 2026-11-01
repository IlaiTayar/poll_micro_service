from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Question(BaseModel):
    question_id: int
    poll_id: int
    question_text: str