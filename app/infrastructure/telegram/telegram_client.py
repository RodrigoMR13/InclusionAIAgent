from dotenv import load_dotenv
import httpx
import os

load_dotenv(r"C:\Users\Public\repos\Estudos\Faculdade\projeto_aplicado_3\env")
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{API_TOKEN}"
WEBHOOK_PATH = "api/telegram/webhook"

class TelegramClient():
    @staticmethod
    async def send_message(chat_id: str, text: str):
        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/sendMessage"
            payload = {"chat_id": chat_id, "text": text}
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        
    @staticmethod
    async def setup_webhook(ngrok_url: str) -> str:
        try:
            webhook_url = f"{ngrok_url}/{WEBHOOK_PATH}"
            delete_url = f"{BASE_URL}/deleteWebhook"
            set_webhook_url = f"{BASE_URL}/setWebhook?url={webhook_url}"

            async with httpx.AsyncClient() as client:
                delete_response = await client.get(delete_url)
                delete_response.raise_for_status()
                print("Webhook antigo deletado:", delete_response.json())

                set_response = await client.get(set_webhook_url)
                set_response.raise_for_status()
                print("Novo webhook configurado:", set_response.json())
                return set_response.json()
        except Exception as e:
            print(f"Error setting up webhook: {e}")
            return None
