# SIGMA Vision

Sistema de análisis de imágenes digitales como señales bidimensionales mediante filtros de convolución y Transformada de Fourier.

---

## 🧠 Descripción del proyecto

SIGMA Vision es un sistema desarrollado en Python que permite cargar una imagen y procesarla como una **señal bidimensional**.

El sistema aplica conceptos de **Teoría de Sistemas** donde:

- La imagen de entrada representa una señal
- Los filtros representan sistemas LTI (Lineales e Invariantes en el Tiempo)
- La salida corresponde a la señal procesada

---

## ⚙️ Funcionamiento del sistema

1. El usuario carga una imagen desde la interfaz Streamlit
2. La imagen se envía al backend FastAPI
3. Se valida que sea JPG, JPEG o PNG
4. Se guarda en la carpeta `uploads/`
5. Se procesa mediante OpenCV y NumPy
6. Se aplican filtros por convolución y Transformada de Fourier
7. Se generan imágenes de salida en `resultados/`
8. La interfaz muestra los resultados con sus descripciones técnicas

---

## 🔬 Procesamiento aplicado

### ⬛ Escala de grises
Convierte la imagen de color (BGR) a una señal de intensidad única para simplificar el análisis.

### 🌫️ Filtro de suavizado — Pasa bajas
Kernel de promedio 3x3. Reduce el ruido reemplazando cada píxel por el promedio de sus vecinos.

### 🌀 Filtro Gaussiano — Pasa bajas
Suavizado con distribución gaussiana. Da más peso al píxel central, produciendo un resultado más natural.

### 🔆 Filtro pasa altas
Se obtiene restando el gaussiano a la imagen original. Conserva solo los detalles finos, bordes y texturas.

### 🔪 Filtro de enfoque — Sharpening
Kernel de realce. Resalta cambios bruscos de intensidad aumentando el contraste en los bordes.

### 📐 Detección de bordes — Laplaciano
Kernel Laplaciano. Detecta cambios fuertes de intensidad en todas las direcciones.

### 📊 Transformada de Fourier
FFT 2D que convierte la imagen al dominio de frecuencia. Permite analizar componentes de baja y alta frecuencia espacial.

---

## 🛠️ Tecnologías utilizadas

- Python
- FastAPI
- Streamlit
- OpenCV
- NumPy
- Pillow
- Requests

---

## 📦 Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/proyecto_teoria.git
cd proyecto_teoria
```

### 2. Instalar dependencias

```bash
pip install -r requisitos.txt
```

### 3. Correr el backend (FastAPI)

```bash
uvicorn menu:app --reload
```

El backend quedará disponible en: `http://127.0.0.1:8000`

### 4. Correr la interfaz (Streamlit)

Abre una segunda terminal y ejecuta:

```bash
streamlit run interfaz.py
```

La interfaz abrirá automáticamente en: `http://localhost:8501`

> ⚠️ Ambas terminales deben estar corriendo al mismo tiempo.

---

## 🌐 Despliegue en la nube

El proyecto está dividido en dos servicios desplegados por separado:

### Backend — Render
- Plataforma: [render.com](https://render.com)
- Se conecta al repositorio de GitHub
- Despliega automáticamente con cada `git push`

### Interfaz — Streamlit Cloud
- Plataforma: [streamlit.io/cloud](https://streamlit.io/cloud)
- Se conecta al repositorio de GitHub
- Despliega la interfaz automáticamente

---

## 📡 API del sistema

### GET `/`
Verifica que el servidor esté activo.

```json
{
  "mensaje": "SIGMA Vision funcionando correctamente"
}
```

### POST `/procesar`
Recibe una imagen y devuelve las rutas de los resultados con sus descripciones técnicas.

**Parámetros:**
- `archivo` — imagen en formato JPG, JPEG o PNG

**Respuesta:**
```json
{
  "mensaje": "Procesamiento completado",
  "original": "uploads/imagen.jpg",
  "original_descripcion": "...",
  "gris": "resultados/imagen_gris.jpg",
  "gris_descripcion": "...",
  "suavizada": "resultados/imagen_suavizada.jpg",
  "suavizada_descripcion": "...",
  "gaussiana": "resultados/imagen_gaussiana.jpg",
  "gaussiana_descripcion": "...",
  "pasa_altas": "resultados/imagen_pasa_altas.jpg",
  "pasa_altas_descripcion": "...",
  "enfocada": "resultados/imagen_enfocada.jpg",
  "enfocada_descripcion": "...",
  "bordes": "resultados/imagen_bordes.jpg",
  "bordes_descripcion": "...",
  "fourier": "resultados/espectro_fourier.jpg",
  "fourier_descripcion": "...",
  "comparacion": {
    "entrada": "uploads/imagen.jpg",
    "sistema": "Convolución con kernels + Transformada de Fourier 2D",
    "salidas": ["..."]
  }
}
```

---

## 📁 Estructura del proyecto

```
proyecto_teoria/
├── menu.py          # Servidor FastAPI (backend)
├── proyecto.py      # Lógica de procesamiento de imágenes
├── interfaz.py      # Interfaz visual con Streamlit
├── requisitos.txt   # Dependencias del proyecto
├── uploads/         # Imágenes subidas por el usuario
└── resultados/      # Imágenes procesadas generadas
```
