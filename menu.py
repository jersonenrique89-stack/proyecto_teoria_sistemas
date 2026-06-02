from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from fastapi.staticfiles import StaticFiles

from proyecto import procesar_imagen

import os

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

    ruta = f"uploads/{archivo.filename}"

    contenido = await archivo.read()

    with open(ruta, "wb") as f:
        f.write(contenido)

    resultado = procesar_imagen(ruta)

    return resultado