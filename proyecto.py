import cv2
import os
import numpy as np
import base64


def imagen_a_base64(imagen_array):
    """Convierte un array de imagen OpenCV a string base64."""
    _, buffer = cv2.imencode(".jpg", imagen_array)
    return base64.b64encode(buffer).decode("utf-8")


def procesar_imagen(ruta_imagen):
    print("***** EJECUTANDO PROYECTO.PY *****")
    print("Ruta recibida:", ruta_imagen)

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

    # Aplicar filtro Gaussiano
    # (5, 5) es el tamaño del kernel, 1 es la desviación estándar en X y Y
    imagen_gaussiana = cv2.GaussianBlur(
        imagen_gris,
        (5, 5),
        1
    )

    # Aplicar filtro pasa altas
    # Se resta la imagen gaussiana (bajas frecuencias) a la imagen original
    # El resultado contiene solo las altas frecuencias (detalles y bordes)
    imagen_pasa_altas = cv2.subtract(imagen_gris, imagen_gaussiana)

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

    # --- CONVERTIR IMÁGENES A BASE64 ---
    # Las imágenes se codifican en base64 para enviarlas directamente en la respuesta
    # sin necesidad de guardarlas en disco de forma permanente
    original_b64   = imagen_a_base64(imagen)
    gris_b64       = imagen_a_base64(imagen_gris)
    suavizada_b64  = imagen_a_base64(imagen_suavizada)
    gaussiana_b64  = imagen_a_base64(imagen_gaussiana)
    pasa_altas_b64 = imagen_a_base64(imagen_pasa_altas)
    enfocada_b64   = imagen_a_base64(imagen_enfocada)
    bordes_b64     = imagen_a_base64(imagen_bordes)
    fourier_b64    = imagen_a_base64(espectro)

    # --- ELIMINAR IMAGEN SUBIDA ---
    # El sistema no almacena imágenes de forma permanente
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)

    # Devolver las imágenes en base64 junto con explicaciones técnicas
    return {
        "mensaje": "Procesamiento completado",

        # --- IMAGEN ORIGINAL ---
        "original": original_b64,
        "original_descripcion": (
            "Imagen de entrada al sistema. Representa la señal bidimensional "
            "original antes de aplicar cualquier transformación o filtro."
        ),

        # --- ESCALA DE GRISES ---
        "gris": gris_b64,
        "gris_descripcion": (
            "La imagen se convierte de color (BGR) a escala de grises. "
            "Cada píxel representa la intensidad luminosa. Esto simplifica "
            "el análisis tratando la imagen como una señal de un solo canal."
        ),

        # --- FILTRO PASA BAJAS: SUAVIZADO PROMEDIO ---
        "suavizada": suavizada_b64,
        "suavizada_descripcion": (
            "Filtro pasa bajas mediante convolución con un kernel de promedio 3x3. "
            "Cada píxel se reemplaza por el promedio de sus vecinos. "
            "Elimina el ruido y atenúa las altas frecuencias espaciales."
        ),

        # --- FILTRO PASA BAJAS: GAUSSIANO ---
        "gaussiana": gaussiana_b64,
        "gaussiana_descripcion": (
            "Filtro pasa bajas gaussiano con kernel 5x5. "
            "Aplica mayor peso al píxel central y menor a los bordes del kernel. "
            "Produce un suavizado más natural y uniforme que el promedio simple."
        ),

        # --- FILTRO PASA ALTAS ---
        "pasa_altas": pasa_altas_b64,
        "pasa_altas_descripcion": (
            "Filtro pasa altas obtenido restando la imagen gaussiana a la original. "
            "Elimina las bajas frecuencias y conserva únicamente los detalles finos, "
            "bordes y texturas de la imagen."
        ),

        # --- FILTRO DE REALCE (ENFOQUE) ---
        "enfocada": enfocada_b64,
        "enfocada_descripcion": (
            "Filtro de realce por convolución con kernel sharpening. "
            "Aumenta el contraste en zonas de cambio brusco de intensidad, "
            "resaltando los detalles y bordes de la imagen."
        ),

        # --- FILTRO DE DETECCIÓN DE BORDES ---
        "bordes": bordes_b64,
        "bordes_descripcion": (
            "Filtro de detección de bordes mediante kernel Laplaciano. "
            "Detecta cambios fuertes de intensidad en todas las direcciones. "
            "El resultado resalta los contornos y límites de los objetos."
        ),

        # --- ESPECTRO DE FOURIER ---
        "fourier": fourier_b64,
        "fourier_descripcion": (
            "Transformada de Fourier 2D aplicada a la imagen en grises. "
            "Convierte la imagen del dominio espacial al dominio de frecuencia. "
            "El centro del espectro representa las bajas frecuencias y los bordes "
            "las altas frecuencias. Permite analizar la distribución de frecuencias "
            "espaciales de la imagen."
        ),

        # --- COMPARACIÓN ENTRADA VS SALIDA ---
        "comparacion": {
            "sistema": "Convolución con kernels + Transformada de Fourier 2D"
        }
    }
