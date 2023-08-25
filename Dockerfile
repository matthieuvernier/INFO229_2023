# Utiliza la imagen base oficial de Python
FROM python:3.8

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY main.py /app/main.py

# Instala las dependencias
RUN pip install fastapi uvicorn

# Expone el puerto en el que se ejecuta la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
