from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException

from fastapi.staticfiles import StaticFiles

from proyecto import procesar_imagen

import os

FORMATOS_PERMITIDOS = {".jpg", ".jpeg", ".png"}

app = FastAPI(
    title="SIGMA Vision",
    description="Backend de procesamiento de imágenes",
    version="1.0"
)

# Crear carpetas
os.makedirs("uploads", exist_ok=True)
os.makedirs("resultados", exist_ok=True)

# Mostrar resultados como archivos estáticos
app.mount(
    "/resultados",
    StaticFiles(directory="resultados"),
    name="resultados"
)


@app.get("/")
def inicio():

    return {
        "mensaje": "SIGMA Vision funcionando correctamente"
    }


@app.post("/procesar")
async def procesar(
    archivo: UploadFile = File(...)
):
    # Validar extensión del archivo
    nombre = archivo.filename or ""
    extension = os.path.splitext(nombre)[1].lower()

    if extension not in FORMATOS_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no permitido: '{extension}'. Solo se aceptan JPG, JPEG o PNG."
        )

    ruta = f"uploads/{nombre}"

    contenido = await archivo.read()

    with open(ruta, "wb") as f:
        f.write(contenido)

    resultado = procesar_imagen(ruta)

    return resultado