import requests

PHP_URL = "https://secura.multillantas.com/WhatsAppChatBotAgent/rptaMenu.php"


class ERP:
    def consultar(self, numero: str, mensaje: str) -> list:
        """
        Llama al PHP con el número y mensaje del cliente.
        Devuelve una lista de mensajes a enviar.
        """
        payload = {
            "query": {
                "sender": numero,
                "message": mensaje,
                "isGroup": False,
                "ruleId": ""
            },
            "appPackageName": "com.whatsapp",
            "messengerPackageName": "com.whatsapp"
        }
        try:
            response = requests.post(PHP_URL, json=payload, timeout=10)
            data = response.json()
            mensajes = [r["message"] for r in data.get("replies", [])]
            return mensajes
        except Exception:
            return ["❌ Error al conectar con el sistema. Intenta más tarde."]
