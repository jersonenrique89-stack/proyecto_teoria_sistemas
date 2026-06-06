# SIGMA Vision

Sistema de análisis de imágenes digitales como señales bidimensionales mediante filtros de convolución y Transformada de Fourier.

---

## 🧠 Descripción del proyecto

SIGMA Vision es un backend desarrollado en Python que permite cargar una imagen y procesarla como una **señal bidimensional**.

El sistema aplica conceptos de **Teoría de Sistemas** donde:

- La imagen de entrada representa una señal
- Los filtros representan sistemas LTI (Lineales e Invariantes en el Tiempo)
- La salida corresponde a la señal procesada

---

## ⚙️ Funcionamiento del sistema

El sistema realiza el siguiente flujo:

1. El usuario carga una imagen
2. La imagen se guarda en la carpeta `uploads/`
3. Se procesa mediante OpenCV
4. Se aplican filtros por convolución
5. Se realiza análisis en frecuencia (Transformada de Fourier)
6. Se generan imágenes de salida en `resultados/`

---

## 🔬 Procesamiento aplicado

### 🖤 Escala de grises
Se convierte la imagen a una señal de intensidad única para simplificar el análisis.

---

### 🌫️ Filtro de suavizado (Blur)
Se aplica un kernel de promedio 3x3:

- Reduce ruido
- Simula un filtro pasa bajas

---

### 🔪 Filtro de enfoque (Sharpening)
Resalta bordes y detalles mediante convolución.

- Realza cambios bruscos de intensidad

---

### 📐 Detección de bordes
Utiliza un kernel tipo Laplaciano:

- Detecta cambios fuertes en la señal
- Representa alta frecuencia espacial

---

### 📊 Transformada de Fourier
Se aplica FFT 2D:

- Convierte la imagen al dominio de frecuencia
- Permite analizar componentes de baja y alta frecuencia
- Se genera un espectro visual

---

## 🛠️ Tecnologías utilizadas

- Python
- FastAPI
- OpenCV
- NumPy

---

## 📡 API del sistema

### 🔹 GET `/`
Verifica que el servidor esté activo.

Respuesta:
```json
{
  "mensaje": "SIGMA Vision funcionando correctamente"
}