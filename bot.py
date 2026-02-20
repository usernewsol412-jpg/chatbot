import re


class Bot:
    def __init__(self):
        self.usuarios = {}  # guarda el nombre de cada número

    def procesar(self, texto: str, numero: str, cliente) -> None:
        texto_lower = texto.strip().lower()

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
            cliente.enviar_mensaje(numero, f"¡Bienvenido, {nombre}! ¿En qué te puedo ayudar?")
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
        if texto_lower == "agente":
            cliente.enviar_mensaje(numero, "👤 En breve un agente te contactará.")
            return

        # Respuesta por defecto
        nombre = self.usuarios.get(numero, "")
        saludo = f"{nombre}, " if nombre else ""
        cliente.enviar_mensaje(numero, f"{saludo}recibí tu mensaje: {texto}")
