import streamlit as st
import requests
from PIL import Image
import io
import base64


def base64_a_imagen(b64_string):
    """Convierte un string base64 a imagen PIL."""
    bytes_img = base64.b64decode(b64_string)
    return Image.open(io.BytesIO(bytes_img))


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
        st.image(base64_a_imagen(datos["gris"]), use_container_width=True)
        st.info(datos.get("gris_descripcion", ""))
        st.divider()

        # --- FILTROS PASA BAJAS ---
        st.subheader("🌫️ Filtros pasa bajas (suavizado)")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Suavizado promedio**")
            st.image(base64_a_imagen(datos["suavizada"]), use_container_width=True)
            st.info(datos.get("suavizada_descripcion", ""))

        with col2:
            st.markdown("**Filtro Gaussiano**")
            st.image(base64_a_imagen(datos["gaussiana"]), use_container_width=True)
            st.info(datos.get("gaussiana_descripcion", ""))

        st.divider()

        # --- FILTROS PASA ALTAS ---
        st.subheader("🔆 Filtros pasa altas")
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Pasa altas**")
            st.image(base64_a_imagen(datos["pasa_altas"]), use_container_width=True)
            st.info(datos.get("pasa_altas_descripcion", ""))

        with col4:
            st.markdown("**Realce / Enfoque**")
            st.image(base64_a_imagen(datos["enfocada"]), use_container_width=True)
            st.info(datos.get("enfocada_descripcion", ""))

        st.divider()

        # --- DETECCIÓN DE BORDES ---
        st.subheader("📐 Detección de bordes")
        st.image(base64_a_imagen(datos["bordes"]), use_container_width=True)
        st.info(datos.get("bordes_descripcion", ""))
        st.divider()

        # --- ESPECTRO DE FOURIER ---
        st.subheader("📊 Espectro de Fourier")
        st.image(base64_a_imagen(datos["fourier"]), use_container_width=True)
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
            st.image(base64_a_imagen(datos["bordes"]), use_container_width=True)

    else:
        # Mostrar error del backend
        st.error(f"❌ Error: {respuesta.json().get('detail', 'Error desconocido')}")
