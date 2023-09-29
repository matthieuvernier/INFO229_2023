class Grabacion:
    def __init__(self, nombre, fecha, duracion, descripcion=""):
        self.nombre = nombre
        self.fecha = fecha
        self.duracion = duracion
        self.descripcion = descripcion
        self.transcripcion = None  # Inicialmente, la transcripción es None

    def agregar_descripcion(self, descripcion):
        self.descripcion = descripcion

    def obtener_descripcion(self):
        return self.descripcion

    def agregar_transcripcion(self, transcripcion):
        self.transcripcion = transcripcion

    def obtener_transcripcion(self):
        return self.transcripcion
