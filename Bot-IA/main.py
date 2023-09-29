# Importa la clase OpenAITranscriber desde el archivo openai_transcriber.py
from transcripcion.transcriber import OpenAITranscriber
# Importa la clase Grabacion desde el archivo grabacion.py
from transcripcion.grabacion import Grabacion

# Crear una instancia de OpenAITranscriber
transcriber = OpenAITranscriber()

# Cargar un archivo MP3 desde la ubicación deseada
nombre_archivo_mp3 = "audiofiles/clase1_programacion_hectorferrada_1.mp3"

# Realizar la transcripción
transcripcion = transcriber.transcribir_audio(nombre_archivo_mp3)

if transcripcion:
    print("Transcripción:")
    print(transcripcion)

    # Crear un objeto Grabacion y agregarlo a una lista de grabaciones
    nueva_grabacion = Grabacion("Clase de Programacion", "2023-09-30", "1 minuto")
    nueva_grabacion.agregar_descripcion("Una clase de Héctor Ferrada")

    # Agregar la nueva grabación a una lista de grabaciones
    lista_de_grabaciones = []
    lista_de_grabaciones.append(nueva_grabacion)

    print("Nueva grabación agregada a la lista de grabaciones.")
else:
    print("No se pudo obtener la transcripción.")
