# main.py
from fastapi import FastAPI
from routes.usuarios import ruta_usuarios

app = FastAPI()

app.include_router(ruta_usuarios)

@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Usuarios en funcionamiento"}