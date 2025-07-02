from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from fastapi.responses import JSONResponse
from app.auth import verify_token, authenticate_user, register_user
from app.ocr import extract_health_data
from app.database import reports_collection
from app.models import report_doc
from jose import jwt
import os
from typing import List
from bson.objectid import ObjectId
from datetime import datetime
from collections import defaultdict

router = APIRouter()

# ✅ Register new user
@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    await register_user(username, password)
    return {"message": f"User '{username}' registered successfully"}

# ✅ Login and return JWT token
@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if not await authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": username}, os.getenv("SECRET_KEY"), algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# ✅ Upload report (PDF/image), run OCR, save to DB
@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    current_user: str = Depends(verify_token)
):
    content = await file.read()
    result = extract_health_data(file.filename, content)

    report_data = report_doc(current_user, file.filename, result)
    await reports_collection.insert_one(report_data)

    return {
        "user": current_user,
        "filename": file.filename,
        "extracted": result
    }

@router.get("/reports")
async def get_user_reports(current_user: str = Depends(verify_token)):
    cursor = reports_collection.find({"owner": current_user})
    reports = []
    async for report in cursor:
        reports.append({
            "id": str(report["_id"]),
            "filename": report["filename"],
            "timestamp": report["timestamp"].strftime("%Y-%m-%d %H:%M"),
            "extracted": report["extracted"]
        })
    if not reports:
        raise HTTPException(status_code=404, detail="No reports found")
    return {"user": current_user, "reports": reports}


@router.get("/trends")
async def get_health_trends(current_user: str = Depends(verify_token)):
    cursor = reports_collection.find({"owner": current_user}).sort("timestamp", 1)

    trends = defaultdict(lambda: {"timestamps": [], "values": []})
    async for report in cursor:
        date = report["timestamp"].strftime("%Y-%m-%d")
        extracted = report.get("extracted", {})
        for param, values in extracted.items():
            trends[param]["timestamps"].append(date)
            trends[param]["values"].append(values.get("value"))

    return {"user": current_user, "trends": trends}
