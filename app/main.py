from fastapi import FastAPI
from app.routes import tasks

app = FastAPI(title="AI Task Manager Engine")

app.include_router(tasks.router)