from pydantic import BaseModel
from .message import _Message


class Event(BaseModel):
    type: str
    event: _Message
