import re


class Bot:
    def __init__(self):
        self.usuarios = {}  # guarda el nombre de cada número

    def procesar(self, texto: str, numero: str) -> str:
        texto_lower = texto.strip().lower()

        # Saludo
        if re.search(r"^(hola|hi|hey|buenas|buenos días|buenas tardes|buenas noches)[\s!?]*$", texto_lower):
            return "¡Hola! 👋 Brindame tu nombre para darte un servicio personalizado."

        # El cliente manda su nombre
        match = re.search(r"^(mi nombre es|me llamo|soy)\s+(.+)$", texto_lower)
        if match:
            nombre = match.group(2).strip().capitalize()
            self.usuarios[numero] = nombre
            return f"¡Bienvenido, {nombre}! ¿En qué te puedo ayudar?"

        # Si ya sabemos su nombre, lo usamos
        nombre = self.usuarios.get(numero, "")
        saludo = f"{nombre}, " if nombre else ""

        # Agrega más reglas aquí:
        # if re.search(r"precio|costo|cuánto", texto_lower):
        #     return f"{saludo}nuestros precios están en nuestra web."

        return f"{saludo}recibí tu mensaje: {texto}"
