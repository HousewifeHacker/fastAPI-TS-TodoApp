# standard lib

# 3rd party
from pydantic import BaseModel, Field

# local
from app.enums import Priority


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

class Token(BaseModel):
    access_token: str
    type: str = "bearer"

class TodoCreate(BaseModel):
    title: str
    priority: Priority
    completed: bool = False
    user_id: int

class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int
    priority: Priority