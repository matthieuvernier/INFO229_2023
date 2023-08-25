from fastapi import FastAPI, Query

app = FastAPI()

# Lista de veterinarias (simulación de almacenamiento de datos)
veterinarias = []

@app.get("/")
async def root():
    return {"message": "Hola InfoPet!"}

class Veterinaria:
    def __init__(self, nombre: str, direccion: str):
        self.nombre = nombre
        self.direccion = direccion

@app.post("/veterinaria/")
def agregar_veterinaria(nombre: str, direccion: str):
    nueva_veterinaria = Veterinaria(nombre=nombre, direccion=direccion)
    veterinarias.append(nueva_veterinaria)
    return {"message": "Veterinaria agregada exitosamente"}

@app.delete("/veterinaria/")
def eliminar_veterinaria(nombre: str):
    global veterinarias
    veterinarias = [v for v in veterinarias if v.nombre != nombre]
    return {"message": "Veterinaria eliminada exitosamente"}

@app.get("/veterinarias/")
def listar_veterinarias(direccion: str = Query(None, description="Filtrar por dirección")):
    if direccion:
        return [{"nombre": v.nombre, "direccion": v.direccion} for v in veterinarias if v.direccion == direccion]
    else:
        return [{"nombre": v.nombre, "direccion": v.direccion} for v in veterinarias]
