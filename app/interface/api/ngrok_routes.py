from fastapi import APIRouter, Query
from app.infrastructure.ngrok.ngrok_service import NgrokService

ngrok_router = APIRouter()
ngrok_service = NgrokService()

@ngrok_router.get("/tunnels")
async def get_ngroks_active():
    response = ngrok_service.list_active_tunnels()
    if response == []:
        return {"warning": "Nenhum túnel ativo"}
    
    return {"ok": True, "tunnels": [t.public_url for t in response]}


@ngrok_router.delete("/tunnels")
async def delete_all_ngroks():
    response = ngrok_service.delete_all_tunnels()
    if not response:
        return {"warning": "Nenhum túnel ativo para deletar."}
    
    return {"ok": True, "message": "Todos os túneis foram deletados."}

@ngrok_router.delete("/tunnels/item")
async def delete_ngrok(name_or_url: str = Query(..., description="URL pública ou nome do túnel")):
    response = ngrok_service.delete_tunnel(name_or_url)
    if not response:
        return {"warning": "Nenhum túnel ativo para deletar."}

    return {"ok": True, "message": "Túnel deletado com sucesso."}

@ngrok_router.post("/tunnels/setup")
async def setup_ngrok():
    response = ngrok_service.setup_ngrok()
    if response is None:
        return {"error": "Failed to set up ngrok"}
    
    return {"ok": True, "ngrok_url": response}