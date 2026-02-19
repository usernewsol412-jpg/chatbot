from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Estos valores los completás con los de Meta
VERIFY_TOKEN = "mi_token_secreto"
ACCESS_TOKEN = "AQUI_VA_TU_TOKEN_DE_META"
PHONE_ID = "AQUI_VA_TU_PHONE_ID"

@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params["hub.challenge"])
    return {"error": "token inválido"}

@app.post("/webhook")
async def recibir_mensaje(request: Request):
    data = await request.json()
    try:
        mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]
        numero = mensaje["from"]
        texto = mensaje["text"]["body"]
        responder(numero, f"Recibí tu mensaje: {texto}")
    except:
        pass
    return {"status": "ok"}

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
