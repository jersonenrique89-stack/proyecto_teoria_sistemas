# Importaciones de FastAPI para crear la API y manejar archivos
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException

# Para servir archivos estáticos (las imágenes resultantes)
from fastapi.staticfiles import StaticFiles

# Función principal de procesamiento de imágenes
from proyecto import procesar_imagen

import os

# Extensiones de imagen permitidas para la carga
FORMATOS_PERMITIDOS = {".jpg", ".jpeg", ".png"}

# Crear la aplicación FastAPI con su título y descripción
app = FastAPI(
    title="SIGMA Vision",
    description="Backend de procesamiento de imágenes",
    version="1.0"
)

# Crear las carpetas necesarias si no existen
os.makedirs("uploads", exist_ok=True)    # Carpeta donde se guardan las imágenes subidas
os.makedirs("resultados", exist_ok=True) # Carpeta donde se guardan las imágenes procesadas

# Exponer la carpeta "resultados" como archivos accesibles por URL
# Ejemplo: http://127.0.0.1:8000/resultados/imagen_gris.jpg
app.mount(
    "/resultados",
    StaticFiles(directory="resultados"),
    name="resultados"
)


# Endpoint raíz — verifica que el servidor está funcionando
@app.get("/")
def inicio():
    return {
        "mensaje": "SIGMA Vision funcionando correctamente"
    }


# Endpoint principal — recibe una imagen, la valida y la procesa
@app.post("/procesar")
async def procesar(
    archivo: UploadFile = File(...)  # El archivo viene del cuerpo del formulario
):
    # Obtener el nombre del archivo y su extensión
    nombre = archivo.filename or ""
    extension = os.path.splitext(nombre)[1].lower()

    # Validar que la extensión sea JPG, JPEG o PNG
    if extension not in FORMATOS_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no permitido: '{extension}'. Solo se aceptan JPG, JPEG o PNG."
        )

    # Definir la ruta donde se guardará la imagen subida
    ruta = f"uploads/{nombre}"

    # Leer el contenido binario del archivo
    contenido = await archivo.read()

    # Guardar la imagen en la carpeta uploads
    with open(ruta, "wb") as f:
        f.write(contenido)

    # Enviar la imagen al módulo de procesamiento y obtener los resultados
    resultado = procesar_imagen(ruta)

    # Devolver las rutas de las imágenes generadas
    return resultado
