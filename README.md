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
2. El usuario selecciona los filtros que desea aplicar
3. La imagen se envía al backend FastAPI
4. Se valida que sea JPG, JPEG o PNG
5. Se procesa mediante OpenCV y NumPy
6. Se aplican solo los filtros seleccionados por convolución y Transformada de Fourier
7. Las imágenes resultantes se devuelven en base64 (sin guardar en disco)
8. La interfaz muestra los resultados con sus descripciones técnicas
9. La imagen subida se elimina automáticamente al finalizar

---

## 🔬 Procesamiento aplicado

### ⬛ Escala de grises
Convierte la imagen de color (BGR) a una señal de intensidad única para simplificar el análisis.

### 🌫️ Filtro de suavizado — Pasa bajas (Convolución)
Kernel de promedio 3x3. Reduce el ruido reemplazando cada píxel por el promedio de sus vecinos.

### 🌀 Filtro Gaussiano — Pasa bajas
Suavizado con distribución gaussiana 5x5. Da más peso al píxel central, produciendo un resultado más natural.

### 🔆 Filtro pasa altas
Se obtiene restando el gaussiano a la imagen original. Conserva solo los detalles finos, bordes y texturas.

### 🔪 Filtro de enfoque — Sharpening (Convolución)
Kernel de realce. Resalta cambios bruscos de intensidad aumentando el contraste en los bordes.

### 📐 Detección de bordes — Laplaciano (Convolución)
Kernel Laplaciano. Detecta cambios fuertes de intensidad en todas las direcciones.

### 📊 Transformada de Fourier
FFT 2D que convierte la imagen al dominio de frecuencia. Permite analizar componentes de baja y alta frecuencia espacial.

---

## 🛠️ Tecnologías utilizadas

- Python
- FastAPI (backend / API REST)
- Streamlit (interfaz gráfica)
- OpenCV (procesamiento de imágenes)
- NumPy (operaciones numéricas)
- Pillow (visualización de imágenes en Streamlit)
- Requests (comunicación entre Streamlit y FastAPI)

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

### 3. Correr el backend (Terminal 1)

```bash
uvicorn menu:app --reload
```

El backend quedará disponible en: `http://127.0.0.1:8000`

Para ver la documentación de la API: `http://127.0.0.1:8000/docs`

### 4. Correr la interfaz (Terminal 2)

```bash
streamlit run interfaz.py
```

La interfaz abrirá automáticamente en: `http://localhost:8501`

> ⚠️ Ambas terminales deben estar corriendo al mismo tiempo.

---

## 🖥️ Uso del sistema

1. Abrir la interfaz en `http://localhost:8501`
2. Subir una imagen JPG, JPEG o PNG
3. Seleccionar los filtros que se quieren aplicar (checkboxes)
4. Hacer clic en "Procesar imagen"
5. Ver los resultados con sus explicaciones técnicas
6. Comparar visualmente la imagen original vs las salidas procesadas

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
Recibe una imagen y los filtros a aplicar. Devuelve las imágenes en base64.

**Parámetros:**
- `archivo` — imagen en formato JPG, JPEG o PNG (obligatorio)
- `filtros` — filtros separados por comas (opcional, si no se envía aplica todos)
  - Valores posibles: `gris`, `suavizada`, `gaussiana`, `pasa_altas`, `enfocada`, `bordes`, `fourier`

**Ejemplo de filtros:**
```
gris,suavizada,bordes,fourier
```

---

## 🔒 Restricciones cumplidas

- ✅ No realiza reconocimiento facial
- ✅ No identifica personas por nombre
- ✅ No almacena imágenes de forma permanente
- ✅ No almacena información personal del usuario
- ✅ No crea bases de datos biométricas
- ✅ El enfoque es análisis de imagen como señal bidimensional

---

## 📁 Estructura del proyecto

```
proyecto_teoria/
├── menu.py          # Servidor FastAPI (backend / API)
├── proyecto.py      # Lógica de procesamiento de imágenes
├── interfaz.py      # Interfaz visual con Streamlit
├── requisitos.txt   # Dependencias del proyecto
├── README.md        # Documentación del proyecto
├── uploads/         # Carpeta temporal (se vacía automáticamente)
└── resultados/      # Carpeta legacy (no se usa con base64)
```

---

## 🌐 Despliegue en la nube (opcional)

### Backend — Render
- Plataforma: [render.com](https://render.com)
- Se conecta al repositorio de GitHub
- Despliega automáticamente con cada `git push`

### Interfaz — Streamlit Cloud
- Plataforma: [streamlit.io/cloud](https://streamlit.io/cloud)
- Se conecta al repositorio de GitHub
- Despliega la interfaz automáticamente
