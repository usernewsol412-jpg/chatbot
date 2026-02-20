import re
import os
import time
from erp import ERP

TIMEOUT_AGENTE = 30 #* 60  # 30 minutos (cambia este valor cuando quieras)


class Bot:
    def __init__(self):
        self.usuarios = {}       # guarda el nombre de cada número
        self.en_agente = {}      # numero -> timestamp de cuando fue derivado al agente
        self.agente = os.environ.get("AGENT_NUMBER", "")
        self.erp = ERP()

    def procesar(self, texto: str, numero: str, cliente) -> None:
        texto_lower = texto.strip().lower()

        # Si el agente escribe "fin", libera al último cliente en cola
        if numero == self.agente and texto_lower == "fin":
            if self.en_agente:
                numero_cliente = next(iter(self.en_agente))
                del self.en_agente[numero_cliente]
                cliente.enviar_mensaje(numero_cliente, "✅ La atención ha finalizado. ¡Gracias por contactarnos! Si necesitas algo más escribe *hola*.")
            return

        # Si el cliente está en modo agente, verificar timeout
        if numero in self.en_agente:
            tiempo_en_agente = time.time() - self.en_agente[numero]
            if tiempo_en_agente > TIMEOUT_AGENTE:
                del self.en_agente[numero]
                cliente.enviar_mensaje(numero, "✅ La sesión con el agente ha finalizado. Si necesitas algo más escribe *hola*.")
                # Ya fue liberado, continuar procesando el mensaje normalmente
            else:
                return

        # Saludo
        if re.search(r"^(hola|hi|hey|buenas|buenos días|buenas tardes|buenas noches)[\s!?]*$", texto_lower):
            if numero in self.usuarios:
                nombre = self.usuarios[numero]
                cliente.enviar_mensaje(numero, f"¡Hola de nuevo, {nombre}! ¿En qué te puedo ayudar?")
            else:
                cliente.enviar_mensaje(numero, "¡Hola! 👋 Brindame tu nombre para darte un servicio personalizado.")
            return

        # El cliente manda su nombre
        match = re.search(r"^(mi nombre es|me llamo|soy)\s+(.+)$", texto_lower)
        if match:
            nombre = match.group(2).strip().capitalize()
            self.usuarios[numero] = nombre
            cliente.enviar_mensaje(numero, f"¡Bienvenido, {nombre}! ¿En qué te puedo ayudar?\nEscriba menú  si desea ver todas las opciones.")
            return

        # Menú
        if re.search(r"^(menú|menu|opciones)[\s!?]*$", texto_lower):
            cliente.enviar_lista(
                numero=numero,
                texto="¿En qué te puedo ayudar? Selecciona una opción:",
                boton="Ver opciones",
                secciones=[
                    {
                        "title": "Servicios",
                        "rows": [
                            {"id": "precios", "title": "Ver precios", "description": "Consulta nuestros precios"},
                            {"id": "horarios", "title": "Ver horarios", "description": "Nuestros horarios de atención"},
                            {"id": "ubicacion", "title": "Ubicación", "description": "Dónde estamos"},
                        ]
                    },
                    {
                        "title": "Soporte",
                        "rows": [
                            {"id": "agente", "title": "Hablar con agente", "description": "Te conectamos con una persona"},
                        ]
                    }
                ]
            )
            return

        # Respuestas del menú
        if texto_lower == "precios":
            cliente.enviar_mensaje(numero, "💰 Nuestros precios son...")
            return
        if texto_lower == "horarios":
            cliente.enviar_mensaje(numero, "🕐 Atendemos de lunes a viernes de 9am a 6pm.")
            return
        if texto_lower == "ubicacion":
            cliente.enviar_mensaje(numero, "📍 Estamos ubicados en...")
            return

        # Derivar a agente
        if texto_lower == "agente":
            nombre = self.usuarios.get(numero, "Cliente")
            self.en_agente[numero] = time.time()
            cliente.enviar_mensaje(numero, "👤 Un agente te contactará pronto. Por favor espera 😊")
            cliente.enviar_mensaje(self.agente, f"🔔 *Nueva conversación*\nCliente: *{nombre}*\nNúmero: +{numero}\n\nCuando termines escribe: *fin*")
            return

        # Consultar al ERP
        mensajes = self.erp.consultar(numero, texto)
        for msg in mensajes:
            cliente.enviar_mensaje(numero, msg)
