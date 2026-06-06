import cv2
import os
import numpy as np


def procesar_imagen(ruta_imagen):
    print("***** EJECUTANDO PROYECTO.PY *****")
    print("Ruta recibida:", ruta_imagen)

   

    os.makedirs("resultados", exist_ok=True)

    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        return {"error": "No se pudo cargar la imagen"}

    # Escala de grises
    imagen_gris = cv2.cvtColor(
        imagen,
        cv2.COLOR_BGR2GRAY
    )

    # Kernel suavizado
    kernel_suavizado = np.ones(
        (3, 3),
        np.float32
    ) / 9

    # Kernel enfoque
    kernel_enfoque = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    # Kernel bordes
    kernel_bordes = np.array([
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ])

    # --- FILTRO PASA ALTAS ---
    # Kernel 3x3 que elimina componentes de baja frecuencia
    # y resalta bordes y detalles finos (altas frecuencias espaciales).
    # La suma del kernel es 1, por lo que preserva la luminosidad media
    # mientras amplifica los cambios bruscos de intensidad.
    kernel_pasa_altas = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])

    # Aplicar filtros
    imagen_suavizada = cv2.filter2D(
        imagen_gris,
        -1,
        kernel_suavizado
    )

    imagen_enfocada = cv2.filter2D(
        imagen_gris,
        -1,
        kernel_enfoque
    )

    imagen_bordes = cv2.filter2D(
        imagen_gris,
        -1,
        kernel_bordes
    )

    # --- APLICAR FILTRO PASA ALTAS ---
    # Se aplica el kernel pasa altas por convolución sobre la imagen en grises.
    # El resultado resalta bordes y texturas, suprimiendo las zonas uniformes.
    imagen_pasa_altas = cv2.filter2D(
        imagen_gris,
        -1,
        kernel_pasa_altas
    )

    # Fourier
    f = np.fft.fft2(imagen_gris)
    fshift = np.fft.fftshift(f)

    espectro = 20 * np.log(
        np.abs(fshift) + 1
    )

    espectro = cv2.normalize(
        espectro,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    espectro = espectro.astype(np.uint8)

    # Guardar imágenes
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

    # --- GUARDAR RESULTADO PASA ALTAS ---
    # Se exporta la imagen filtrada a la carpeta de resultados.
    cv2.imwrite(
        "resultados/imagen_pasa_altas.jpg",
        imagen_pasa_altas
    )

    return {
        "mensaje": "Procesamiento completado",
        "gris": "resultados/imagen_gris.jpg",
        "suavizada": "resultados/imagen_suavizada.jpg",
        "enfocada": "resultados/imagen_enfocada.jpg",
        "bordes": "resultados/imagen_bordes.jpg",
        "fourier": "resultados/espectro_fourier.jpg",
        "pasa_altas": "resultados/imagen_pasa_altas.jpg"
    }