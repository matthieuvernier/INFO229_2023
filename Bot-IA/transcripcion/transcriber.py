import openai

class Transcriber:
    def transcribir_audio(self, archivo_audio):
        pass

class OpenAITranscriber(Transcriber):
    api_key = "..."

    def __init__(self):
        openai.api_key = self.api_key

    def transcribir_audio(self, archivo_audio):
        try:
            modelo = "whisper-1"
            # Asegúrate de abrir el archivo en modo binario "rb"
            with open(archivo_audio, "rb") as audio_file:
                print(audio_file)
                # Realizar la transcripción utilizando la librería openai
                response = openai.Audio.transcribe(modelo, audio_file)

                # Verificar si la transcripción se completó con éxito
                if response.get("text") is not None:
                    transcripcion = response["text"]
                    return transcripcion
                else:
                    print(f"Error en la solicitud: {response.get('error')}")
                    return None

        except Exception as e:
            print(f"Error en la solicitud: {str(e)}")
            return None

class CustomTranscriber(Transcriber):
    def transcribir_audio(self, archivo_audio):
        # Implementación personalizada para otro servicio de transcripción
        # Puedes usar otra librería o API aquí
        pass
