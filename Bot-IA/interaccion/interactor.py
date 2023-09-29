import openai

class Interactor:
    def ask(self, pregunta):
        pass

class OpenAIInteractor(Interactor):
    api_key = "..."

    def __init__(self):
        openai.api_key = self.api_key

    def ask(self, pregunta): 
        # Llama a la API de OpenAI para obtener una respuesta a la pregunta
        respuesta = openai.Completion.create(
                engine="text-davinci-002",  # Puedes usar el motor que desees
                prompt=pregunta,
                max_tokens=500  # Ajusta el número de tokens máximos según tus necesidades
            )
        return respuesta