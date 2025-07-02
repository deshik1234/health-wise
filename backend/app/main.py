from fastapi import FastAPI
from app.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Health Report API", version="1.0")

# Enable CORS for frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(api_router)
