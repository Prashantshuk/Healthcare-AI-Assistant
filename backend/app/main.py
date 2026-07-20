from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
import app.models
from app.api.upload import router as upload_router
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.chat import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare AI Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(upload_router)

@app.get("/")
def root():
    return {"message": "Healthcare AI Assistant Backend is Running"}