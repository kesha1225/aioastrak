from pydantic import BaseModel
from .message import MessageEvent


class Event(BaseModel):
    type: str
    event: MessageEvent
