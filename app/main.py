from fastapi import FastAPI
from app.interface.api.ai_routes import ai_router
from app.interface.api.telegram_routes import telegram_router
from app.interface.api.ngrok_routes import ngrok_router

app = FastAPI(title="Inclusion AI Chatbot POC")

app.include_router(ai_router, prefix="/api/ai", tags=["AI"])
app.include_router(telegram_router, prefix="/api/telegram", tags=["Telegram"])
app.include_router(ngrok_router, prefix="/api/ngrok", tags=["Ngrok"])