import discord
import openai
from discord.ext import commands
from pydub import AudioSegment

import sys
import os
directorio_transcripcion = os.path.join(os.path.dirname(__file__), '..', 'transcripcion')
sys.path.append(directorio_transcripcion)
directorio_interaccion = os.path.join(os.path.dirname(__file__), '..', 'interaccion')
sys.path.append(directorio_interaccion)

from transcriber import OpenAITranscriber
from grabacion import Grabacion

from interactor import OpenAIInteractor

class BotDiscord:
    _instance = None

    # Crea una instancia de OpenAIInteractor
    openai_interactor = OpenAIInteractor()

    # Almacenaremos las grabaciones en una lista
    lista_de_grabaciones = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BotDiscord, cls).__new__(cls)
            cls._instance._intents = discord.Intents.default()
            cls._instance._intents.message_content = True

            cls._instance._bot = commands.Bot(command_prefix='!', intents=cls._instance._intents)
            cls._instance._bot.add_command(cls._instance.donuts)
            cls._instance._bot.add_command(cls._instance.transcripcion)
            cls._instance._bot.add_command(cls._instance.nueva_grabacion)
            cls._instance._bot.add_command(cls._instance.pregunta)

            cls._instance._token = "..."

            @cls._instance._bot.event
            async def on_ready():
                print(f'Conectado como {cls._instance._bot.user.name}')

        return cls._instance

    @property
    def donuts(self):
        @commands.command()
        async def donuts(ctx):
            await ctx.send('Mmm... donuts.')
        return donuts


    @property
    def transcripcion(self):
        @commands.command()
        async def transcripcion(ctx):
            print("inicio transcripcion")
            # Verificar si se adjuntó un archivo MP3 al comando
            if not ctx.message.attachments:
                await ctx.send("Por favor, adjunta un archivo MP3 para la transcripción.")
                return

            # Obtener el primer archivo adjunto (asumimos que es un archivo MP3)
            file = ctx.message.attachments[0]

            print(file)

            await file.save('audio.mp3')

            # Realizar la transcripción utilizando OpenAITranscriber
            transcriber = OpenAITranscriber()
            transcripcion = transcriber.transcribir_audio("audio.mp3")

            # Enviar la transcripción en el chat de Discord
            if transcripcion:
                await ctx.send("Transcripción:")
                await ctx.send(transcripcion)
            else:
                await ctx.send("No se pudo obtener la transcripción.")
        return transcripcion

    @property
    def nueva_grabacion(self):
        @commands.command()
        async def nueva_grabacion(ctx, nombre, fecha, descripcion):
             # Verificar si se adjuntó un archivo MP3 al comando
            if not ctx.message.attachments:
                await ctx.send("Por favor, adjunta un archivo MP3 para la transcripción.")
                return

            # Obtener el primer archivo adjunto (asumimos que es un archivo MP3)
            file = ctx.message.attachments[0]

            print(file)

            # Guardar el archivo de audio localmente
            archivo_audio = 'audio.mp3'
            await file.save(archivo_audio)

            # Obtener la duración del archivo de audio utilizando pydub
            audio = AudioSegment.from_mp3(archivo_audio)
            duracion = len(audio)  # Duración en milisegundos

            # Realizar la transcripción utilizando OpenAITranscriber
            transcriber = OpenAITranscriber()
            transcripcion = transcriber.transcribir_audio(archivo_audio)

            # Crear un objeto Grabacion con los datos proporcionados
            grabacion = Grabacion(nombre, fecha, duracion, descripcion)
            grabacion.agregar_transcripcion(transcripcion)

            # Enviar la transcripción y los detalles de la grabación en el chat de Discord
            if transcripcion:
                await ctx.send("Transcripción:")
                await ctx.send(transcripcion)

                # Puedes enviar los detalles de la grabación
                await ctx.send(f"Nombre: {grabacion.nombre}")
                await ctx.send(f"Fecha: {grabacion.fecha}")
                await ctx.send(f"Duración: {grabacion.duracion} ms")
                await ctx.send(f"Descripción: {grabacion.descripcion}")

                # Agregar la grabación a la lista de grabaciones (Seria mejor agregarla en una base de datos)
                self.lista_de_grabaciones.append(grabacion)

            else:
                await ctx.send("No se pudo obtener la transcripción.")

            # Eliminar el archivo de audio temporal
            os.remove(archivo_audio)
        return nueva_grabacion

    @property
    def pregunta(self):
        @commands.command()
        async def pregunta(ctx, *, pregunta):
            try:
               
                 # Llama al método ask del interactor
                instruccion="Basándote sobre el contexto que te doy a continuación, responda a la pregunta."
                #context="contexto: finita de instrucciones para realizar una tarea específica. Son instrucciones concretas, es una secuencia, estamos hablando de algoritmos secuenciales. Ese tipo de algoritmos debemos a trabajar nosotros, no otro tipo de algoritmos. Y los algoritmos que vemos nosotros se llaman algoritmos determinísticos. ¿Qué quiere decir que un algoritmo sea determinístico? Que si yo el algoritmo lo ejecuto una vez con una data de entrada y me da una salida, si yo lo ejecuto nuevamente con la misma data de entrada, tiene que darme la misma salida. Si lo vuelvo a ejecutar con la misma data de entrada, tiene que darme la misma salida. Eso es determinístico. No estamos hablando de algoritmos aleatorizados o algoritmos probabilísticos, que para una misma entrada me dan diferentes respuestas. Esos son otro tipo de algoritmos que quedan excluidos de este curso. Por tanto, estamos hablando de algoritmos determinísticos. Eso creo que no está en las diapositivas, así que usted tiene que ir tomando apuntes también. Secuencia finita de instrucciones para realizar una tarea específica. Un algoritmo, en el fondo, lo que es es una receta. Y una receta, ¿qué es lo que hace? Es la forma, los pasos a seguir, las instrucciones y la secuencia ordenada de cómo se resuelve una tarea, cómo se hace algo, cómo hacer algo. Por ejemplo, una receta para, qué sé yo..."
                context="contexto: El proyecto FUSA lo que hace es identificar las fuentes sonoras ambientales, permite un análisis por medio de redes neuronales, o sea, de un sistema de inteligencia artificial. Lo que estamos viendo es la composición en términos de cuáles son los elementos que suenan, ya sean naturales, artificiales, el ruido de tránsito vehicular o aquellas fuentes que pueden ser contaminantes. Uno de los principales desafíos, aparte del desarrollo técnico, de trabajar con inteligencia artificial, donde unimos elementos acústicos e informáticos, está en que este proyecto incluye a cinco entidades asociadas al Ministerio del Ambiente del sector público, como una mirada hacia dónde se proyecta la política en control del ruido ambiental, y cuatro empresas que tienen funciones distintas y dan servicio en términos de monitoreo de ruido. Por ejemplo, para detectar un cierto evento dentro de un audio, uno tendría que programar el detector, pero programar ese detector es muy difícil porque los datos acústicos son muy complicados. Entonces..."
                 
                pregunta="pregunta:"+pregunta
                respuesta = self.openai_interactor.ask(instruccion+"\n"+context+"\n"+pregunta)

                # Envía la respuesta en el chat de Discord
                await ctx.send("Respuesta:")
                await ctx.send(respuesta.choices[0].text)

            except Exception as e:
                await ctx.send(f"Ocurrió un error al hacer la pregunta: {str(e)}")

        return pregunta



    def run(self):
        self._bot.run(self._token)

if __name__ == "__main__":
    bot = BotDiscord()
    bot.run()
