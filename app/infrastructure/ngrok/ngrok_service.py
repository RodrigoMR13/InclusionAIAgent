import os
from dotenv import load_dotenv
from pyngrok import ngrok, conf

load_dotenv(r"C:\Users\Public\repos\Estudos\Faculdade\projeto_aplicado_3\env")
PORT = 8000
NGROK_PATH = os.getenv("NGROK_PATH")

class NgrokService:
    def __init__(self):
        conf.get_default().ngrok_path = NGROK_PATH

    def setup_ngrok(self) -> bool:
        try:
            public_url = ngrok.connect(PORT, bind_tls=True).public_url
            print(f"ngrok rodando em: {public_url}")
            return public_url
        except Exception as e:
            print(f"Error setting up ngrok: {e}")
            return None
        
    def list_active_tunnels(self) -> list:
        try:
            tunnels = ngrok.get_tunnels()
            if not tunnels:
                print("Nenhum túnel ativo.")
                return []
            print("Túneis ngrok ativos:")
            for t in tunnels:
                print(f"- Nome: {t.name}, URL pública: {t.public_url}, Porta local: {t.config['addr']}")
            return tunnels
        except Exception as e:
            print(f"Error listing tunnels: {e}")
            return []
    
    def delete_tunnel(self, name_or_url: str) -> bool:
        try:
            tunnels = ngrok.get_tunnels()
            for t in tunnels:
                if t.name == name_or_url or t.public_url == name_or_url:
                    ngrok.disconnect(t.public_url)
                    print(f"Túnel '{t.public_url}' deletado")
                    return True
            print(f"Túnel '{name_or_url}' não encontrado")
            return False
        except Exception as e:
            print(f"Error deleting tunnel: {e}")
            return False
    
    def delete_all_tunnels(self) -> bool:
        try:
            tunnels = ngrok.get_tunnels()
            if not tunnels:
                print("Nenhum túnel ativo para deletar.")
                return False
            for t in tunnels:
                ngrok.disconnect(t.public_url)
                print(f"Túnel '{t.public_url}' deletado")
            print("Todos os túneis foram deletados.")
            return True
        except Exception as e:
            print(f"Error deleting all tunnels: {e}")
            return False