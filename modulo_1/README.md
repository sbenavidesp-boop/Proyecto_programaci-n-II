# Proyecto_programaci-n-II
# Calculadora de Masa Molecular
Calculadora de masa molecular para fórmulas químicas, con interfaz gráfica en Python. Permite calcular la masa molecular de cualquier compuesto químico, utilizando una tabla periódica integrada y la posibilidad de añadir elementos personalizados.

# *Características*

1. Interfaz gráfica sencilla y amigable (Tkinter).
2. Reconocimiento automático de elementos y coeficientes en fórmulas químicas.
3. Soporte para paréntesis y grupos químicos complejos.
4. Tabla periódica integrada (con respaldo local y posibilidad de usar librerías externas como periodictable o mendeleev).

# *Instalación*

1. Clona el repositorio o descarga los archivos necesarios.
2. Instala Python 3 (recomendado 3.7+).
3. Instala las dependencias opcionales para mejorar la tabla periódica:
     Shellpip install periodictable mendeleev

*Si no instalas estas librerías, la calculadora usará una tabla local básica.*



# *Uso*
1. Ejecuta el archivo principal:
   Shellpython calculadora.py
2. Se abrirá una ventana donde puedes ingresar la fórmula química (por ejemplo: H2O, C6H12O6, Fe2(SO4)3, CuSO4·5H2O) y presionar "Calcular" para obtener la masa molecular.

# *Ejemplo de entrada*

1. H2O → Agua
2. C6H12O6 → Glucosa
3. Fe2(SO4)3 → Sulfato de hierro(III)
4. CuSO4·5H2O → Sulfato de cobre(II) pentahidratado

*Asegurate de que los elementos estén escritos correctamente, si tiene 2 letras la primera tiene que estar en mayúscula, y si sólo tiene una esta tiene que estar en mayúscula.*
# *Estructura del proyecto*

calculadora.py: Código principal de la calculadora.

# *Créditos*
Desarrollado por Sofía Benavides, Nicolás Spiter, Miguel Millán, Sergio Preciado Y Juan Caviedes
# *Licencia*
Este proyecto se distribuye bajo la licencia MIT. Puedes usarlo, modificarlo y compartirlo libremente.
