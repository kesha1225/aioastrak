from pydantic import BaseModel


class Dialog(BaseModel):
    id: int
    username: str
    last_message: str
    time: int
    last_user: int
    unread_count: int


class DialogMessage(BaseModel):
    read: bool
    message_id: int
    to_id: int
    from_id: int
    created_at: int
    text: str
