# CHEMIQ - Calculadora de masa molecular

**CHEMIQ** es una aplicación en Python que permite calcular la **masa molecular** de fórmulas químicas, con una interfaz gráfica agradable y fácil de usar.

Incluye la instalación automática de las librerías necesarias, tabla periódica de respaldo, historial de cálculos y un diagrama de flujo que representa el proceso por el cual se representa el proceso de cálculo y funcionamiento del programa.


## Características principales
- **Interfaz gráfica (Tkinter)** con degradado y botones interactivos.
- **Diagrama de flujo animado** que muestra el recorrido de datos en el programa.
- **Instalación automática de dependencias** si no están presentes en el entorno.
- **Cálculo automático de masa molecular** a partir de cualquier fórmula química válida.
- **Tabla periódica integrada**, con soporte para librerías externas: periodictable y mendeleev.
- **Historial de cálculos** guardado en formato JSON.


## Requisitos
- Python **3.8 o superior**
- Las siguientes librerías (se instalan automáticamente si no existen):
  ```bash
  pip install periodictable mendeleev pillow


## Ejemplos de uso

En la interfaz principal, puedes ingresar cualquiera de las siguientes fórmulas:

- H2O	(Agua)
- (NH4)2SO4	(Sulfato de amonio)
- Fe2(SO4)3·9H2O	(Sulfato férrico nonahidratado)
- K4[Fe(CN)6]	(Ferricianuro de potasio)


 ## Funciones principales
- calcular_masa_molecular(formula): devuelve la masa molecular total.
- agregar_a_historial(formula, masa): guarda el resultado en el historial.
- abrir_historial(): muestra los cálculos previos en una ventana.
- abrir_flujo_datos(): despliega un diagrama interactivo del proceso de cálculo.

## Créditos
Desarrollado por Sofía Benavides, Nicolás Spiter, Miguel Millán, Sergio Preciado Y Juan Caviedes
