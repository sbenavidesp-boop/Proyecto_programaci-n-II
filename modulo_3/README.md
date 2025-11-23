# CHEMIQ – Calculadora de Masa Molecular

CHEMIQ es una aplicación en Python que permite calcular masas moleculares a partir de fórmulas químicas, analizar resultados, visualizar datos mediante gráficas y mantener un historial de cálculos. Incluye una clasificación automática basada en reglas simples y comparación con datos previos.

## Características principales

### Cálculo de masa molecular
- Soporte para paréntesis (), corchetes [] y llaves {}.
- Soporte para hidratos utilizando punto o punto medio.
- Acepta coeficientes globales.
- Selección automática entre periodictable, mendeleev o tabla periódica local.

### Interfaz gráfica con Tkinter
- Ventana principal con diseño en degradado.
- Entrada para fórmulas químicas.
- Botones de cálculo, ayuda, historial, análisis y flujo de datos.
- Soporte opcional para mostrar un logo.

### Historial de cálculos
- Registra la fórmula ingresada, la masa molecular y la fecha y hora.
- Los datos se guardan en archivo JSON.
- Vista interactiva con opción para eliminar todo el historial.

### Clasificación automática
- Determina si la masa es baja, media o alta.
- Estima si el compuesto es orgánico o inorgánico.
- Compara la masa actual con valores previos para contextualizar resultados.

### Módulo de análisis gráfico
- Histograma de compuestos orgánicos e inorgánicos.
- Gráfico con las cinco fórmulas más calculadas.
- Línea temporal de las masas calculadas.
- Implementado con pandas y matplotlib.

### Diagrama de flujo interactivo
- Presenta el proceso completo desde la entrada del usuario hasta el almacenamiento en historial.
- Incluye animaciones dentro de una ventana Tkinter.

## Requisitos
- Python 3.8 o superior.
- Tkinter instalado por defecto en la mayoría de sistemas.
- Instalación automática de librerías:
  - periodictable
  - mendeleev
  - pandas
  - matplotlib

## Cómo ejecutar
1. Clonar el repositorio:
   git clone https://github.com/sbenavidesp-boop/Proyecto_programaci-n-II

2. Ejecutar la aplicación:
   python CHEMIQ00.py

## Estructura del proyecto

CHEMIQ/
├── CHEMIQ00.py  
├── historial.json  
├── LOGO-removebg-preview.png  
└── README.md  

## Tecnologías utilizadas
- Python
- Tkinter
- Matplotlib
- Pandas
- Periodictable o Mendeleev
- JSON

## Créditos
Desarrollado por Nicolás Spiter, Miguel Millán, Sofía Benavides, Sergio Preciado Y Juan Caviedes

