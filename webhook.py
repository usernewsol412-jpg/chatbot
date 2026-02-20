from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from bot import Bot
from whatsapp import WhatsAppClient
import os

router = APIRouter()
bot = Bot()
cliente = WhatsAppClient()

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mi_token_secreto")


@router.get("/webhook")
async def verificar_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(content=params["hub.challenge"])
    return PlainTextResponse(content="token inválido", status_code=403)


@router.post("/webhook")
async def recibir_mensaje(request: Request):
    data = await request.json()
    try:
        mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]
        numero = mensaje["from"]
        texto = mensaje["text"]["body"]
        respuesta = bot.procesar(texto, numero)
        cliente.enviar_mensaje(numero, respuesta)
    except:
        pass
    return {"status": "ok"}
