from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.schemas import Token, UserCreate
from app.dependencies import DBSession
from app.models import User
from app.auth import hash_pw, verify_pw

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register")
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

@router.post("/login")
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