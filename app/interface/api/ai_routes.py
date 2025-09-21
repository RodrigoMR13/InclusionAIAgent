from fastapi import APIRouter
from app.application.use_cases.process_message import ProcessMessageUseCase
from app.domain.entities.message import Message
from app.infrastructure.ai.geminiai_service import GeminiAIService
from app.interface.api.schemas import MessageSchema

ai_router = APIRouter()
process_message_use_case = ProcessMessageUseCase(ai_service=GeminiAIService())

@ai_router.post("/chat")
async def chat(message: MessageSchema):
    response = await process_message_use_case.execute(Message(chat_id="123", text=message.text))
    return {"reply": response}