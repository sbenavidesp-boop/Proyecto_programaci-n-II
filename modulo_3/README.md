 1  # CHEMIQ – Calculadora de Masa Molecular
 2  
 3  CHEMIQ es una aplicación interactiva en Python que calcula masas moleculares,
 4  analiza resultados, guarda historial y genera gráficas. Incluye una mini-IA
 5  que contextualiza cada cálculo según datos previos.
 6  
 7  ## Características principales
 8  
 9  ### Cálculo de masa molecular
10  - Soporta (), [], {}.
11  - Soporta hidratos con punto o punto medio (·, .).
12  - Acepta coeficientes globales, como 2FeSO4.
13  - Usa automáticamente periodictable, mendeleev o la tabla local.
14  
15  ### Interfaz gráfica (Tkinter)
16  - Ventana principal con degradado.
17  - Entrada para fórmulas.
18  - Botones de cálculo, ayuda, historial, análisis y diagrama de flujo.
19  - Soporte opcional para logo.
20  
21  ### Historial de cálculos
22  - Registra fórmula, masa molecular y timestamp.
23  - Se guarda en historial.json.
24  - Vista interactiva con opción para limpiar historial.
25  
26  ### Mini-IA de clasificación
27  - Clasifica la masa como baja, media o alta.
28  - Determina si el compuesto es orgánico o inorgánico.
29  - Compara la masa con valores previos y genera análisis contextual.
30  
31  ### Módulo de análisis gráfico
32  - Histograma de compuestos orgánicos vs. inorgánicos.
33  - Top 5 fórmulas más calculadas.
34  - Gráfica temporal de masas moleculares.
35  - Utiliza pandas y matplotlib.
36  
37  ### Diagrama de flujo interactivo
38  - Muestra el recorrido completo: usuario → entrada → cálculo → resultado → historial.
39  - Animaciones progresivas dentro de una ventana Tkinter.
40  
41  ## Requisitos
42  - Python 3.8+
43  - Tkinter (ya está incluido en la mayoría de sistemas).
44  - Las librerías necesarias se instalan automáticamente al ejecutar:
45    - periodictable
46    - mendeleev
47    - pandas
48    - matplotlib
49  
50  ##  Cómo ejecutar
51  1. Clona el repositorio:
52     git clone https://github.com/tuusuario/turepo.git
53  
54  2. Ejecuta la aplicación:
55     python CHEMIQ00.py
56  
57  La interfaz gráfica se abrirá automáticamente.
58  
59  ##  Estructura del proyecto recomendada
60  
61  📁 CHEMIQ/
62  ├── CHEMIQ00.py
63  ├── historial.json         # generado automáticamente
64  ├── LOGO-removebg-preview.png   # opcional
65  └── README.md
66  
67  ##  Tecnologías usadas
68  - Python
69  - Tkinter
70  - Matplotlib
71  - Pandas
72  - Periodictable / Mendeleev
73  - JSON
74  
75  ## 📌 Licencia
76  Puedes agregar una licencia aquí (MIT, GPL, etc.).
