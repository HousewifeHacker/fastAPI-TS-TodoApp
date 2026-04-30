# standard lib

# 3rd party
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import select

# local
from app.database import engine, Base
from app.dependencies import DBSession
from app.schemas import TodoCreate, TodoOut, UserCreate, Token
from app.models import Todo, User
from app.auth import hash_pw, verify_pw


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown code: nothing needed for now

app = FastAPI(lifespan=lifespan)

@app.get("/dummy_ok")
async def dummy():
    return {"status": "ok"}

@app.post("/register")
async def register(
    user: UserCreate,
    db: DBSession
) -> dict :
    new_user = User(
        username=user.username,
        password=hash_pw(user.password)
    )

    db.add(new_user)
    await db.commit()

    return {"message": "registered"}

@app.post("/login")
async def login(
    user: UserCreate,
    db: DBSession
) -> Token:
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_pw(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Placeholder token generation, replace with actual JWT generation
    token = "fake-jwt-token-for-" + db_user.username
    return Token(access_token=token)

@app.post("/todos")
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

@app.get("/todos")
async def list_todos(
    db: DBSession
) -> list[TodoOut]:
    #TODO filter todos by authenticated user
    result = await db.execute(select(Todo))
    todos = result.scalars().all()
    return todos