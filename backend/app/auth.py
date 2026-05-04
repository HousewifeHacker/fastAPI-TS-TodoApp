import os
import dotenv
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

dotenv.load_dotenv()
hashing_key = os.getenv("hashing_key")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def hash_pw(password: str) -> str:
    # Placeholder for hashing function, replace with actual hashing (e.g., bcrypt)
    return pwd_context.hash(password)

def verify_pw(password: str, hashed_password: str) -> bool:
    # Placeholder for password verification function
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # Placeholder for JWT token creation
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data["exp"] = expire
    return jwt.encode(data, hashing_key, algorithm="HS256")

def verify_access_token(token: str) -> dict:
    # Placeholder for JWT token verification
    return jwt.decode(token, hashing_key, algorithms=["HS256"])

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = verify_access_token(token)
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return username

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )