from fastapi import APIRouter
from sqlalchemy import select

from app.schemas import TodoCreate, TodoOut
from app.dependencies import DBSession
from app.models import Todo

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_todo(
    todo: TodoCreate,
    db: DBSession
) -> TodoOut:
    #TODO associate the todo with the authenticated user
    new_todo = Todo(
        title=todo.title,
        priority=todo.priority,
        completed=todo.completed,
        owner_id=todo.user_id
    )
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo

@router.get("/")
async def list_todos(
    db: DBSession
) -> list[TodoOut]:
    #TODO filter todos by authenticated user
    result = await db.execute(select(Todo))
    todos = result.scalars().all()
    return todos