# Proyecto_programaci-n-II
Calculadora de Masa Molecular
Calculadora de masa molecular para fórmulas químicas, con interfaz gráfica en Python. Permite calcular la masa molecular de cualquier compuesto químico, utilizando una tabla periódica integrada y la posibilidad de añadir elementos personalizados.
Características

Interfaz gráfica sencilla y amigable (Tkinter).
Reconocimiento automático de elementos y coeficientes en fórmulas químicas.
Soporte para paréntesis y grupos químicos complejos.
Tabla periódica integrada (con respaldo local y posibilidad de usar librerías externas como periodictable o mendeleev).
Personalización: puedes añadir nuevos elementos y sus masas atómicas si no están en la tabla.
Persistencia: los elementos personalizados se guardan en un archivo tabla_custom.json.

Instalación

Clona el repositorio o descarga los archivos necesarios.
Instala Python 3 (recomendado 3.7+).
Instala las dependencias opcionales para mejorar la tabla periódica:
Shellpip install periodictable mendeleevMostrar más líneas

Si no instalas estas librerías, la calculadora usará una tabla local básica.



Uso
Ejecuta el archivo principal:
Shellpython calculadora.pyMostrar más líneas
Se abrirá una ventana donde puedes ingresar la fórmula química (por ejemplo: H2O, C6H12O6, Fe2(SO4)3, CuSO4·5H2O) y presionar Calcular para obtener la masa molecular.
Ejemplo de entrada

H2O → Agua
C6H12O6 → Glucosa
Fe2(SO4)3 → Sulfato de hierro(III)
CuSO4·5H2O → Sulfato de cobre(II) pentahidratado

Personalización
Si ingresas un elemento que no está en la tabla, el programa te permitirá añadirlo manualmente, guardando la información para futuros cálculos.
Estructura del proyecto

calculadora.py: Código principal de la calculadora.
tabla_custom.json: Archivo generado automáticamente para guardar elementos personalizados.

Créditos
Desarrollado por Sofía Benavides Pedraza.
Licencia
Este proyecto se distribuye bajo la licencia MIT. Puedes usarlo, modificarlo y compartirlo libremente.
