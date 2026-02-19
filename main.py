from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
import os

app = FastAPI()

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mi_token_secreto")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
PHONE_ID = os.environ.get("PHONE_ID", "")

@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(content=params["hub.challenge"])
    return PlainTextResponse(content="token inválido", status_code=403)

@app.post("/webhook")
async def recibir_mensaje(request: Request):
    data = await request.json()
    try:
        mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]
        numero = mensaje["from"]
        texto = mensaje["text"]["body"]
        respuesta = procesar_mensaje(texto)
        responder(numero, respuesta)
    except:
        pass
    return {"status": "ok"}

def procesar_mensaje(texto: str) -> str:
    texto_lower = texto.strip().lower()
    if texto_lower in ["hola", "hola!", "hola?", "hi", "hey"]:
        return "¡Hola! 👋 Bienvenido. ¿En qué te puedo ayudar?"
    return f"Recibí tu mensaje: {texto}"

def responder(numero, texto):
    url = f"https://graph.facebook.com/v22.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    body = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, json=body, headers=headers)
