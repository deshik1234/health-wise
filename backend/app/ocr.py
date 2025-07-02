import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io
import re

def extract_health_data(filename: str, content: bytes):
    text = ""

    if filename.lower().endswith(".pdf"):
        images = convert_from_bytes(content)
        for img in images:
            text += pytesseract.image_to_string(img)
    elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(image)
    else:
        return {"error": "Unsupported file format"}

    return parse_health_parameters(text)

def parse_health_parameters(text):
    parameters = {
        "Hemoglobin": {"unit": "g/dL", "range": "13.0-17.0"},
        "WBC": {"unit": "cells/uL", "range": "4000-11000"},
        "Glucose": {"unit": "mg/dL", "range": "70-110"}
    }

    extracted = {}

    for param, meta in parameters.items():
        match = re.search(rf"{param}\s*[:\-]?\s*(\d+\.?\d*)", text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            low, high = map(float, meta["range"].split("-"))
            status = "Needs Attention" if not (low <= value <= high) else "Normal"
            extracted[param] = {
                "value": value,
                "unit": meta["unit"],
                "range": meta["range"],
                "status": status
            }

    return extracted
