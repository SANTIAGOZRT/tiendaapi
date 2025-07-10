from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.usuarios import ruta_usuarios

app = FastAPI()

# Orígenes permitidos
origins = [
    "https://tiendaapi-k6cj.onrender.com",
    # puedes añadir más como "http://localhost:4200" para desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # define orígenes explícitamente (no usar ["*"] si allow_credentials=True)
    allow_credentials=True,         # si usas cookies o cabeceras de autenticación
    allow_methods=["*"],            # permite todos los métodos HTTP (GET, POST, PUT, DELETE...)
    allow_headers=["*"],            # permite cabeceras personalizadas
)

app.include_router(ruta_usuarios)

@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Usuarios en funcionamiento"}

