from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Dict
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Demo in-memory user store (replace with DB later!)
fake_users: Dict[str, str] = {}

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def authenticate_user(username: str, password: str):
    hashed = fake_users.get(username)
    if not hashed or not pwd_context.verify(password, hashed):
        return False
    return True

def register_user(username: str, password: str):
    if username in fake_users:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pw = pwd_context.hash(password)
    fake_users[username] = hashed_pw
