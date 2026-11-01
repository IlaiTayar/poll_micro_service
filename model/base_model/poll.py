from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Poll(BaseModel):
    poll_id: int
    poll_name: str