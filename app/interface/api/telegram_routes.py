from fastapi import APIRouter, Query, Request
from app.application.use_cases.static_question import StaticQuestionUseCase
from app.infrastructure.telegram.telegram_client import TelegramClient
from app.application.use_cases.process_message import ProcessMessageUseCase
from app.infrastructure.ai.geminiai_service import GeminiAIService
from app.domain.entities.message import Message

telegram_router = APIRouter()
process_message_use_case = ProcessMessageUseCase(ai_service=GeminiAIService())

@telegram_router.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    chat_id = str(data["message"]["chat"]["id"])
    user_text = data["message"]["text"]
    if user_text == "/iniciar":
        disclaimer = ("\nOlá, eu sou o InclusionAI 🤖✨\n\n"
            "Meu objetivo é fornecer informações e orientações sobre inclusão educacional para crianças com altas habilidades e superdotação.\n\n"
            "Aqui estão algumas perguntas que você pode fazer:\n"
            "1️⃣ O que é superdotação?\n"
            "2️⃣ Como identificar altas habilidades?\n"
            "3️⃣ Quais direitos legais garantem inclusão escolar?\n"
            "4️⃣ Quais estratégias ajudam professores em sala de aula?\n\n"
            "Digite o número da opção ou envie sua pergunta livremente.\n\n"
            "⚠️ Aviso: As respostas fornecidas aqui têm caráter informativo e não substituem a orientação de profissionais especializados em educação, psicologia ou saúde. Sempre consulte especialistas para decisões importantes.")
        await TelegramClient.send_message(chat_id, disclaimer)
        return {"ok": True}
    
    if user_text.isdigit():
        user_text = StaticQuestionUseCase.execute(user_text)

    resposta = await process_message_use_case.execute(Message(chat_id=chat_id, text=user_text))
    await TelegramClient.send_message(chat_id, resposta)

    return {"ok": True}


@telegram_router.post("/webhook/setup")
async def telegram_webhook_setup(ngrok_url: str):
    telegram_response = await TelegramClient.setup_webhook(ngrok_url)
    if (telegram_response is None):
        return {"error": "Failed to set up Telegram webhook"}
    
    return {
        "ok": True,
        "ngrok_url": ngrok_url,
        "telegram_response": telegram_response
    }