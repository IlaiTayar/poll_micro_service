from pydantic import BaseModel


class PollRequest(BaseModel):
    poll_name: str