# standard lib

# 3rd party
from fastapi import FastAPI
from contextlib import asynccontextmanager

# local
from app.database import engine, Base
from app.routers import users_router, todos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown code: nothing needed for now

app = FastAPI(lifespan=lifespan)

#routers
app.include_router(todos_router)
app.include_router(users_router)

@app.get("/dummy_ok")
async def dummy():
    return {"status": "ok"}
