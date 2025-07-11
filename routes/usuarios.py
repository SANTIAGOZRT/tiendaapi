import os
import logging
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from traceback import format_exc

# --- Setup logging básico ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# --- Carga variables de Entorno ---
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("MONGO_DB")

# --- Conexión a MongoDB ---
try:
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
except Exception as e:
    logger.exception("Error conectando a MongoDB")
    raise

# --- FastAPI app ---
app = FastAPI()
ruta_usuarios = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# --- Configuración CORS ---
origins = [
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware para capturar errores no previstos ---
class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as http_exc:
            logger.exception(f"HTTPException en {request.url.path}")
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail},
            )
        except Exception as exc:
            logger.exception(f"ERROR inesperado en {request.url.path}: {format_exc()}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Error interno del servidor"},
            )

app.add_middleware(ExceptionHandlerMiddleware)

# --- Modelo Pydantic ---
class Usuario(BaseModel):
    cedula: str
    nombre: str
    salario: float
    fecha_nacimiento: str
    fecha_ingreso: str
    cargo: str
    banco: Optional[str] = None

# --- Función utilitaria ---
def serializar_usuario(usuario):
    usuario["_id"] = str(usuario["_id"])
    return usuario

# --- Rutas de usuarios ---
@ruta_usuarios.get("/")
def listar_usuarios():
    try:
        usuarios = list(db["usuarios"].find())
        return [serializar_usuario(u) for u in usuarios]
    except Exception as e:
        logger.exception("Fallo listando usuarios")
        raise HTTPException(status_code=500, detail="Error al listar usuarios")

@ruta_usuarios.post("/")
def crear_usuario(usuario: Usuario):
    try:
        print("Recibido:", usuario.dict())
        if db["usuarios"].find_one({"cedula": usuario.cedula}):
            raise HTTPException(status_code=400, detail="La cédula ya está registrada")
        resultado = db["usuarios"].insert_one(usuario.dict())
        return {"mensaje": "Usuario creado exitosamente", "id": str(resultado.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error creando usuario")
        raise HTTPException(status_code=500, detail="Error al crear usuario")


@ruta_usuarios.put("/{cedula}")
def actualizar_usuario(cedula: str, datos: Usuario):
    try:
        resultado = db["usuarios"].update_one({"cedula": cedula}, {"$set": datos.dict()})
        if resultado.matched_count == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mensaje": "Usuario actualizado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error actualizando usuario")
        raise HTTPException(status_code=500, detail="Error al actualizar usuario")

@ruta_usuarios.delete("/{cedula}")
def eliminar_usuario(cedula: str):
    try:
        resultado = db["usuarios"].delete_one({"cedula": cedula})
        if resultado.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mensaje": "Usuario eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error eliminando usuario")
        raise HTTPException(status_code=500, detail="Error al eliminar usuario")

# --- Registrar rutas ---
app.include_router(ruta_usuarios)

@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Usuarios en funcionamiento"}
