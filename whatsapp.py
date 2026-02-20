import requests
import os


class WhatsAppClient:
    def __init__(self):
        self.access_token = os.environ.get("ACCESS_TOKEN", "")
        self.phone_id = os.environ.get("PHONE_ID", "")
        self.url = f"https://graph.facebook.com/v22.0/{self.phone_id}/messages"

    def enviar_mensaje(self, numero: str, texto: str):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        body = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {"body": texto}
        }
        requests.post(self.url, json=body, headers=headers)
