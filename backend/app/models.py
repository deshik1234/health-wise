from datetime import datetime
from typing import List

def user_doc(username: str, hashed_password: str):
    return {
        "username": username,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }

def report_doc(owner: str, filename: str, extracted: dict):
    return {
        "owner": owner,
        "filename": filename,
        "extracted": extracted,
        "timestamp": datetime.utcnow()
    }
