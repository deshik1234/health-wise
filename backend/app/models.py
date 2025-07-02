from datetime import datetime

def report_doc(owner: str, filename: str, extracted: dict):
    return {
        "owner": owner,
        "filename": filename,
        "extracted": extracted,
        "timestamp": datetime.utcnow()
    }
