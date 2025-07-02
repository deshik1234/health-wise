from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from app.database import users_collection
from app.models import user_doc
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Verify JWT token
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# 🔐 Authenticate user with hashed password
async def authenticate_user(username: str, password: str) -> bool:
    user = await users_collection.find_one({"username": username})
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        return False
    return True

# 🔐 Register new user
async def register_user(username: str, password: str):
    existing = await users_collection.find_one({"username": username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = pwd_context.hash(password)
    await users_collection.insert_one(user_doc(username, hashed))
