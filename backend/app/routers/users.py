from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.schemas import Token, UserCreate
from app.dependencies import DBSession
from app.models import User
from app.auth import hash_pw, verify_pw, create_access_token, get_current_user

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
    db: DBSession,
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    result = await db.execute(
        select(User).where(User.username == form_data.username)
    )
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_pw(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)) -> dict:
    # Placeholder for getting current user info, replace with actual logic to extract user from token
    return {"username": current_user}