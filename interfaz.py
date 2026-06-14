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
    st.image(imagen_original, caption="Imagen de entrada al sistema.", use_container_width=True)
    st.divider()

    # --- SELECCIÓN DE FILTROS ---
    st.subheader("🎛️ Selecciona los filtros a aplicar")

    col_filtros1, col_filtros2 = st.columns(2)

    with col_filtros1:
        aplicar_gris = st.checkbox("⬛ Escala de grises", value=True)
        aplicar_suavizado = st.checkbox("🌫️ Suavizado promedio (pasa bajas)", value=True)
        aplicar_gaussiano = st.checkbox("🌀 Filtro Gaussiano (pasa bajas)", value=True)

    with col_filtros2:
        aplicar_pasa_altas = st.checkbox("🔆 Filtro pasa altas", value=True)
        aplicar_enfoque = st.checkbox("🔪 Enfoque / Sharpening", value=True)
        aplicar_bordes = st.checkbox("📐 Detección de bordes", value=True)

    aplicar_fourier = st.checkbox("📊 Transformada de Fourier", value=True)

    st.divider()

    # --- BOTÓN PROCESAR ---
    if st.button("🚀 Procesar imagen", type="primary"):

        # Crear la lista de filtros seleccionados
        filtros_seleccionados = []
        if aplicar_gris:
            filtros_seleccionados.append("gris")
        if aplicar_suavizado:
            filtros_seleccionados.append("suavizada")
        if aplicar_gaussiano:
            filtros_seleccionados.append("gaussiana")
        if aplicar_pasa_altas:
            filtros_seleccionados.append("pasa_altas")
        if aplicar_enfoque:
            filtros_seleccionados.append("enfocada")
        if aplicar_bordes:
            filtros_seleccionados.append("bordes")
        if aplicar_fourier:
            filtros_seleccionados.append("fourier")

        if len(filtros_seleccionados) == 0:
            st.warning("⚠️ Selecciona al menos un filtro para procesar.")
        else:
            # Enviar imagen al backend FastAPI
            with st.spinner("Procesando imagen..."):
                archivo.seek(0)
                respuesta = requests.post(
                    "http://127.0.0.1:8000/procesar",
                    files={"archivo": (archivo.name, archivo, archivo.type)},
                    data={"filtros": ",".join(filtros_seleccionados)}
                )

            # Verificar respuesta
            if respuesta.status_code == 200:
                datos = respuesta.json()
                st.success("✅ Procesamiento completado")
                st.divider()

                # --- ESCALA DE GRISES ---
                if "gris" in datos:
                    st.subheader("⬛ Escala de grises")
                    st.image(base64_a_imagen(datos["gris"]), use_container_width=True)
                    st.info(datos.get("gris_descripcion", ""))
                    st.divider()

                # --- FILTROS PASA BAJAS ---
                mostrar_pasa_bajas = "suavizada" in datos or "gaussiana" in datos
                if mostrar_pasa_bajas:
                    st.subheader("🌫️ Filtros pasa bajas (suavizado)")
                    col1, col2 = st.columns(2)

                    with col1:
                        if "suavizada" in datos:
                            st.markdown("**Suavizado promedio**")
                            st.image(base64_a_imagen(datos["suavizada"]), use_container_width=True)
                            st.info(datos.get("suavizada_descripcion", ""))

                    with col2:
                        if "gaussiana" in datos:
                            st.markdown("**Filtro Gaussiano**")
                            st.image(base64_a_imagen(datos["gaussiana"]), use_container_width=True)
                            st.info(datos.get("gaussiana_descripcion", ""))

                    st.divider()

                # --- FILTROS PASA ALTAS ---
                mostrar_pasa_altas = "pasa_altas" in datos or "enfocada" in datos
                if mostrar_pasa_altas:
                    st.subheader("🔆 Filtros pasa altas")
                    col3, col4 = st.columns(2)

                    with col3:
                        if "pasa_altas" in datos:
                            st.markdown("**Pasa altas**")
                            st.image(base64_a_imagen(datos["pasa_altas"]), use_container_width=True)
                            st.info(datos.get("pasa_altas_descripcion", ""))

                    with col4:
                        if "enfocada" in datos:
                            st.markdown("**Realce / Enfoque**")
                            st.image(base64_a_imagen(datos["enfocada"]), use_container_width=True)
                            st.info(datos.get("enfocada_descripcion", ""))

                    st.divider()

                # --- DETECCIÓN DE BORDES ---
                if "bordes" in datos:
                    st.subheader("📐 Detección de bordes")
                    st.image(base64_a_imagen(datos["bordes"]), use_container_width=True)
                    st.info(datos.get("bordes_descripcion", ""))
                    st.divider()

                # --- ESPECTRO DE FOURIER ---
                if "fourier" in datos:
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
                    st.markdown("**Salida (último filtro aplicado)**")
                    # Mostrar la última imagen disponible como comparación
                    if "bordes" in datos:
                        st.image(base64_a_imagen(datos["bordes"]), use_container_width=True)
                    elif "enfocada" in datos:
                        st.image(base64_a_imagen(datos["enfocada"]), use_container_width=True)
                    elif "pasa_altas" in datos:
                        st.image(base64_a_imagen(datos["pasa_altas"]), use_container_width=True)
                    elif "gris" in datos:
                        st.image(base64_a_imagen(datos["gris"]), use_container_width=True)

            else:
                # Mostrar error del backend
                st.error(f"❌ Error: {respuesta.json().get('detail', 'Error desconocido')}")
