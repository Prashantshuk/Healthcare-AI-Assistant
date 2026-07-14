from fastapi import FastAPI

from app.database.database import Base, engine
import app.models

from app.api.auth import router as auth_router
from app.api.user import router as user_router

from app.api.chat import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare AI Assistant",
    version="1.0.0"
)

app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "Healthcare AI Assistant Backend is Running 🚀"
    }