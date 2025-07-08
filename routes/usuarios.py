import os
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Conexión a MongoDB
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Inicializar FastAPI
app = FastAPI()
ruta_usuarios = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Modelo Pydantic
class Usuario(BaseModel):
    cedula: str
    nombre: str
    salario: float
    fecha_nacimiento: str
    fecha_ingreso: str
    cargo: str
    banco: Optional[str] = None

# Utilidad para convertir ObjectId a str
def serializar_usuario(usuario):
    usuario["_id"] = str(usuario["_id"])
    return usuario

# Listar todos los usuarios
@ruta_usuarios.get("/")
def listar_usuarios():
    usuarios = list(db["usuarios"].find())
    return [serializar_usuario(u) for u in usuarios]

# Crear usuario
@ruta_usuarios.post("/")
def crear_usuario(usuario: Usuario):
    if db["usuarios"].find_one({"cedula": usuario.cedula}):
        raise HTTPException(status_code=400, detail="La cédula ya está registrada")
    
    resultado = db["usuarios"].insert_one(usuario.dict())
    return {"mensaje": "Usuario creado exitosamente", "id": str(resultado.inserted_id)}

# Actualizar usuario por cédula
@ruta_usuarios.put("/{cedula}")
def actualizar_usuario(cedula: str, datos: Usuario):
    resultado = db["usuarios"].update_one({"cedula": cedula}, {"$set": datos.dict()})
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"mensaje": "Usuario actualizado exitosamente"}

# Eliminar usuario por cédula
@ruta_usuarios.delete("/{cedula}")
def eliminar_usuario(cedula: str):
    resultado = db["usuarios"].delete_one({"cedula": cedula})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"mensaje": "Usuario eliminado exitosamente"}


