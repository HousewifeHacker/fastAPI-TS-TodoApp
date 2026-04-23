from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine, Base
from schemas import TodoCreate, UserCreate, Token
from models import Todo, User
from auth import hash_pw, verify_pw


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown code: nothing needed for now

app = FastAPI(lifespan=lifespan)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/dummy_ok")
async def dummy():
    return {"status": "ok"}

@app.post("/register")
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
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
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_pw(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Placeholder token generation, replace with actual JWT generation
    token = "fake-jwt-token-for-" + db_user.username
    return {"access_token": Token(access_token=token)}

@app.post("/todos")
async def create_todo(
    todo: TodoCreate,
    db: AsyncSession = Depends(get_db)
):
    #TODO associate the todo with the authenticated user
    new_todo = Todo(title=todo.title)
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return {"todo": new_todo}

@app.get("/todos")
async def list_todos(
    db: AsyncSession = Depends(get_db)
):
    #TODO filter todos by authenticated user
    result = await db.execute(select(Todo))
    todos = result.scalars().all()
    return {"todos": todos}