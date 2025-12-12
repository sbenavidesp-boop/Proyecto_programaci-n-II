# CHEMIQ – Calculadora Inteligente de Masa Molecular  
**Proyecto Final – Programación de Computadores (2025-II)**  
**Universidad Nacional de Colombia**

---

## Descripción del Proyecto
CHEMIQ es una aplicación en Python diseñada para calcular la masa molecular de compuestos químicos mediante un motor de parsing avanzado capaz de interpretar fórmulas simples y complejas.  
El programa incluye una interfaz gráfica, un sistema de historial persistente, análisis estadístico con gráficos, interpretación automática mediante Mini IA y un diagrama animado del flujo interno del programa.

Este proyecto integra los conocimientos desarrollados a lo largo del curso, combinando estructuras de control, manejo de archivos, modularidad, librerías externas, programación gráfica y análisis de datos.

---

## Características Principales
- Cálculo automático de masa molecular.
- Parser químico recursivo capaz de interpretar:
  - Paréntesis, corchetes y llaves.
  - Grupos anidados.
  - Hidrataciones (·).
- Mini IA que interpreta y contextualiza el resultado.
- Historial persistente almacenado en formato JSON.
- Módulo estadístico con:
  - Histograma de masas.
  - Top 5 de compuestos más frecuentes.
  - Evolución temporal de cálculos.
- Interfaz gráfica construida con Tkinter, con fondo degradado dinámico.
- Visualización animada del flujo interno del programa.
- Sistema de autoinstalación de librerías.

---

## Estructura del Proyecto
CHEMIQ/
│
├── CHEMIQ00.py # Archivo principal del sistema
├── historial.json # Archivo generado automáticamente
├── LOGO.png # Logotipo del programa
└── README.md # Documento descriptivo del proyecto

---

## Funcionamiento General
1. Ejecutar el archivo `CHEMIQ00.py`.
2. El programa verifica e instala automáticamente las librerías necesarias.
3. Se abre la interfaz gráfica principal.
4. El usuario ingresa una fórmula química.
5. El motor de parsing interpreta la estructura del compuesto.
6. El programa calcula la masa molecular utilizando la tabla periódica disponible.
7. La Mini IA genera una interpretación contextual del resultado.
8. El cálculo se almacena en el historial.
9. El usuario puede acceder a:
   - Historial completo.
   - Gráficos analíticos.
   - Diagrama animado del flujo interno.

---

## Tecnologías y Librerías Utilizadas
- Python 3
- Tkinter
- Pillow
- Pandas
- Matplotlib
- periodictable y/o mendeleev
- JSON

---

## 🔬 Módulos Destacados

### 1. Motor de Parsing Químico
Interpreta símbolos químicos, multiplicadores, grupos anidados y compuestos hidratados.  
Ejemplos válidos:
- `Fe2(SO4)3`
- `(NH4)2CO3`
- `K4[Fe(CN)6]`
- `CuSO4·5H2O`

### 2. Historial Persistente
Registra automáticamente:
- Fórmula ingresada
- Masa molecular obtenida
- Fecha y hora en formato ISO  
El historial alimenta el módulo estadístico y la Mini IA.

### 3. Análisis Estadístico
Genera:
- Histograma de distribución de masas calculadas  
- Top 5 compuestos más frecuentes  
- Gráfica temporal de las operaciones realizadas  

---

## Cómo Ejecutar el Programa

### Requisitos
- Python 3.8 o superior
- Conexión a internet si no se tienen las librerías instaladas

### Ejecución
```bash
python CHEMIQ00.py
