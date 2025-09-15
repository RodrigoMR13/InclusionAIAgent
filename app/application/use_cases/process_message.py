from app.domain.entities.message import Message
from app.application.interfaces.ai_service import AIService

class ProcessMessageUseCase:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def execute(self, message: Message) -> str:
        return await self.ai_service.generate_response(message.text)