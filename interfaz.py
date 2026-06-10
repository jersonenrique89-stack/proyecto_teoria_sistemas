import streamlit as st
import requests
from PIL import Image
import io

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="SIGMA Vision",
    page_icon="🔬",
    layout="wide"
)

# --- TÍTULO ---
st.title("🔬 SIGMA Vision")
st.markdown("Sistema de análisis de imágenes digitales como señales bidimensionales.")
st.divider()

# --- SUBIR IMAGEN ---
st.subheader("📤 Cargar imagen")
archivo = st.file_uploader(
    "Selecciona una imagen JPG, JPEG o PNG",
    type=["jpg", "jpeg", "png"]
)

if archivo is not None:

    # Mostrar imagen original
    st.subheader("🖼️ Imagen original")
    imagen_original = Image.open(archivo)
    st.image(imagen_original, caption="Imagen de entrada al sistema. Representa la señal bidimensional original antes de aplicar cualquier transformación.", use_container_width=True)
    st.divider()

    # Enviar imagen al backend FastAPI
    with st.spinner("Procesando imagen..."):
        archivo.seek(0)
        respuesta = requests.post(
            "http://127.0.0.1:8000/procesar",
            files={"archivo": (archivo.name, archivo, archivo.type)}
        )

    # Verificar respuesta
    if respuesta.status_code == 200:
        datos = respuesta.json()
        st.success("✅ Procesamiento completado")
        st.divider()

        # --- ESCALA DE GRISES ---
        st.subheader("⬛ Escala de grises")
        img_gris = requests.get("http://127.0.0.1:8000/resultados/imagen_gris.jpg")
        st.image(Image.open(io.BytesIO(img_gris.content)), use_container_width=True)
        st.info(datos.get("gris_descripcion", ""))
        st.divider()

        # --- COMPARACIÓN: PASA BAJAS ---
        st.subheader("🌫️ Filtros pasa bajas (suavizado)")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Suavizado promedio**")
            img_suavizada = requests.get("http://127.0.0.1:8000/resultados/imagen_suavizada.jpg")
            st.image(Image.open(io.BytesIO(img_suavizada.content)), use_container_width=True)
            st.info(datos.get("suavizada_descripcion", ""))

        with col2:
            st.markdown("**Filtro Gaussiano**")
            img_gaussiana = requests.get("http://127.0.0.1:8000/resultados/imagen_gaussiana.jpg")
            st.image(Image.open(io.BytesIO(img_gaussiana.content)), use_container_width=True)
            st.info(datos.get("gaussiana_descripcion", ""))

        st.divider()

        # --- FILTRO PASA ALTAS ---
        st.subheader("🔆 Filtro pasa altas")
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Pasa altas**")
            img_pasa_altas = requests.get("http://127.0.0.1:8000/resultados/imagen_pasa_altas.jpg")
            st.image(Image.open(io.BytesIO(img_pasa_altas.content)), use_container_width=True)
            st.info(datos.get("pasa_altas_descripcion", ""))

        with col4:
            st.markdown("**Realce / Enfoque**")
            img_enfocada = requests.get("http://127.0.0.1:8000/resultados/imagen_enfocada.jpg")
            st.image(Image.open(io.BytesIO(img_enfocada.content)), use_container_width=True)
            st.info(datos.get("enfocada_descripcion", ""))

        st.divider()

        # --- DETECCIÓN DE BORDES ---
        st.subheader("📐 Detección de bordes")
        img_bordes = requests.get("http://127.0.0.1:8000/resultados/imagen_bordes.jpg")
        st.image(Image.open(io.BytesIO(img_bordes.content)), use_container_width=True)
        st.info(datos.get("bordes_descripcion", ""))
        st.divider()

        # --- ESPECTRO DE FOURIER ---
        st.subheader("📊 Espectro de Fourier")
        img_fourier = requests.get("http://127.0.0.1:8000/resultados/espectro_fourier.jpg")
        st.image(Image.open(io.BytesIO(img_fourier.content)), use_container_width=True)
        st.info(datos.get("fourier_descripcion", ""))
        st.divider()

        # --- COMPARACIÓN ENTRADA VS SALIDA ---
        st.subheader("🔄 Comparación: Entrada vs Salida del sistema")
        comparacion = datos.get("comparacion", {})
        st.markdown(f"**Sistema aplicado:** {comparacion.get('sistema', '')}")

        col_orig, col_result = st.columns(2)

        with col_orig:
            st.markdown("**Entrada (imagen original)**")
            st.image(imagen_original, use_container_width=True)

        with col_result:
            st.markdown("**Salida (bordes detectados)**")
            st.image(Image.open(io.BytesIO(img_bordes.content)), use_container_width=True)

    else:
        # Mostrar error del backend
        st.error(f"❌ Error: {respuesta.json().get('detail', 'Error desconocido')}")
