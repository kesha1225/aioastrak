from pydantic import BaseModel


class MessageEvent(BaseModel):
    message_id: int
    to_id: int
    from_id: int
    created_at: int
    text: str


class Message:
    def __init__(self, message_id, to_id, from_id, created_at, text, api):
        self.message_id = message_id
        self.to_id = to_id
        self.from_id = from_id
        self.created_at = created_at
        self.text = text
        self.api = api

    async def answer(self, text):
        return await self.api.send_message(text=text, to_id=self.from_id)
