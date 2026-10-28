from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Poll(BaseModel):
    poll_id: Optional[int] = None
    poll_name: str


class PollError(Enum):
    NOT_FOUND = "POLL NOT FOUND"
    NAME_EXISTS = "POLL NAME EXISTS"