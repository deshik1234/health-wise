from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from fastapi.responses import JSONResponse
from app.auth import verify_token, authenticate_user, register_user
from app.ocr import extract_health_data
from jose import jwt
import os

# Create API router
router = APIRouter()

# Register new user
@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    register_user(username, password)
    return {"message": f"User '{username}' registered successfully"}

# Login existing user and return JWT token
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": username}, os.getenv("SECRET_KEY"), algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# Upload lab report with auth and extract parameters
@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    current_user: str = Depends(verify_token)
):
    content = await file.read()
    result = extract_health_data(file.filename, content)
    return {
        "user": current_user,
        "filename": file.filename,
        "extracted": result
    }
