import cv2
import os
import numpy as np


def procesar_imagen(ruta_imagen):
    print("***** EJECUTANDO PROYECTO.PY *****")
    print("Ruta recibida:", ruta_imagen)

    # Crear la carpeta de resultados si no existe
    os.makedirs("resultados", exist_ok=True)

    # Cargar la imagen desde la ruta recibida
    imagen = cv2.imread(ruta_imagen)

    # Verificar que la imagen se cargó correctamente
    if imagen is None:
        return {"error": "No se pudo cargar la imagen"}

    # --- ESCALA DE GRISES ---
    # Convierte la imagen de color (BGR) a escala de grises
    # Esto simplifica el análisis tratando la imagen como una señal de intensidad única
    imagen_gris = cv2.cvtColor(
        imagen,
        cv2.COLOR_BGR2GRAY
    )

    # --- KERNEL DE SUAVIZADO (Filtro pasa bajas) ---
    # Kernel de promedio 3x3: cada píxel se reemplaza por el promedio de sus vecinos
    # Efecto: reduce el ruido y suaviza la imagen eliminando altas frecuencias
    kernel_suavizado = np.ones(
        (3, 3),
        np.float32
    ) / 9

    # --- KERNEL DE ENFOQUE (Filtro pasa altas) ---
    # Resalta los detalles y bordes de la imagen
    # Efecto: aumenta el contraste en zonas de cambio brusco de intensidad
    kernel_enfoque = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    # --- KERNEL DE BORDES (Laplaciano) ---
    # Detecta cambios fuertes de intensidad en todas las direcciones
    # Efecto: resalta los contornos y bordes de los objetos en la imagen
    kernel_bordes = np.array([
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ])

    # --- APLICAR FILTROS POR CONVOLUCIÓN ---
    # cv2.filter2D aplica la convolución entre la imagen y el kernel dado

    # Aplicar filtro de suavizado
    imagen_suavizada = cv2.filter2D(
        imagen_gris,
        -1,
        kernel_suavizado
    )

    # Aplicar filtro de enfoque
    imagen_enfocada = cv2.filter2D(
        imagen_gris,
        -1,
        kernel_enfoque
    )

    # Aplicar filtro de detección de bordes
    imagen_bordes = cv2.filter2D(
        imagen_gris,
        -1,
        kernel_bordes
    )

    # --- TRANSFORMADA DE FOURIER 2D ---
    # Convierte la imagen del dominio espacial al dominio de frecuencia
    f = np.fft.fft2(imagen_gris)

    # Desplaza las frecuencias bajas al centro del espectro para mejor visualización
    fshift = np.fft.fftshift(f)

    # Calcular la magnitud del espectro en escala logarítmica
    # Se suma 1 para evitar log(0)
    espectro = 20 * np.log(
        np.abs(fshift) + 1
    )

    # Normalizar los valores del espectro al rango 0-255 para guardarlo como imagen
    espectro = cv2.normalize(
        espectro,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    # Convertir a entero sin signo de 8 bits (formato de imagen estándar)
    espectro = espectro.astype(np.uint8)

    # --- GUARDAR IMÁGENES RESULTANTES ---
    cv2.imwrite(
        "resultados/imagen_gris.jpg",
        imagen_gris
    )

    cv2.imwrite(
        "resultados/imagen_suavizada.jpg",
        imagen_suavizada
    )

    cv2.imwrite(
        "resultados/imagen_enfocada.jpg",
        imagen_enfocada
    )

    cv2.imwrite(
        "resultados/imagen_bordes.jpg",
        imagen_bordes
    )

    cv2.imwrite(
        "resultados/espectro_fourier.jpg",
        espectro
    )

    # Devolver las rutas de todas las imágenes generadas
    return {
        "mensaje": "Procesamiento completado",
        "gris": "resultados/imagen_gris.jpg",
        "suavizada": "resultados/imagen_suavizada.jpg",
        "enfocada": "resultados/imagen_enfocada.jpg",
        "bordes": "resultados/imagen_bordes.jpg",
        "fourier": "resultados/espectro_fourier.jpg"
    }
