FROM python:3.10-slim

# Install OCR & PDF dependencies
RUN apt-get update && \
    apt-get install -y poppler-utils tesseract-ocr && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy all backend files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy Firebase service account (uncomment if deploying to cloud & want it bundled)
# COPY firebase-adminsdk.json /app/firebase-adminsdk.json

# Set Python path so "app.main:app" works
ENV PYTHONPATH=/app

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
