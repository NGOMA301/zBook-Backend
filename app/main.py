
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import summarize
from app.auth import auth_routes

app = FastAPI(title="Book Summarizer API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(summarize.router, prefix="/api/v1/summarize", tags=["Summarize"])
app.include_router(summarize.router, prefix="/api/v1/summaries", tags=["Summaries"])
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Auth"])
