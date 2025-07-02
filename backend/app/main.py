from fastapi import FastAPI
from app.routes import router as api_router

app = FastAPI(title="Health Report API", version="1.0")

app.include_router(api_router)
