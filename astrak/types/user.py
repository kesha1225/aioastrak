from pydantic import BaseModel


class Me(BaseModel):
    token: str
    id: int


class User(BaseModel):
    pass
