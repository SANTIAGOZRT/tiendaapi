from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.usuarios import ruta_usuarios

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes reemplazar "*" con tus dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ruta_usuarios)

@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Usuarios en funcionamiento"}
