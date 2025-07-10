from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.usuarios import ruta_usuarios

app = FastAPI()

# 🌐 Orígenes permitidos para CORS (ajusta según tu entorno)
origins = [
    "http://localhost:4200",              # Para desarrollo local de Angular
    "https://tiendaapi-k6cj.onrender.com", # Producción en Render
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],            # Permite GET, POST, PUT, DELETE, OPTIONS...
    allow_headers=["*"],            # Permite todas las cabeceras que envíe el frontend
)

# Incluir las rutas del router
app.include_router(ruta_usuarios)

@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Usuarios en funcionamiento"}


