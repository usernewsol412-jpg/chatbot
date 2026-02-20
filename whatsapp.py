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

    def enviar_lista(self, numero: str, texto: str, boton: str, secciones: list):
        """
        secciones = [
            {
                "title": "Nombre de sección",
                "rows": [
                    {"id": "opcion_1", "title": "Opción 1", "description": "opcional"},
                    {"id": "opcion_2", "title": "Opción 2"},
                ]
            }
        ]
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        body = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": texto},
                "action": {
                    "button": boton,
                    "sections": secciones
                }
            }
        }
        requests.post(self.url, json=body, headers=headers)
