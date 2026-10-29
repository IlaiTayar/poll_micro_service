from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Poll(BaseModel):
    poll_id: Optional[int] = None
    poll_name: str