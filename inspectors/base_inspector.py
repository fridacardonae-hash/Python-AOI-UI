
class BaseInspector:
    def __init__(self, imagen_absoluta, json_path, config):
        self.imagen_absoluta = imagen_absoluta
        self.json_path = json_path
        self.config = config

    def analizar(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")
