from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

class Token(BaseModel):
    access_token: str

class TodoCreate(BaseModel):
    title: str
    completed: bool = False
    user_id: int

class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int