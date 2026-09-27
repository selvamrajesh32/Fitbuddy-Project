from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import router

app = FastAPI(
    title="FitBuddy AI",
    description="AI-powered personalized fitness planner",
    version="1.0.0"
)

init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)