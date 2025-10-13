# Calculadora de masa molecular
"""
Calculadora de masa molecular :

"""
import tkinter as tk
from tkinter import messagebox
import re
import json
from pathlib import Path

RUTA_CUSTOM = Path("tabla_custom.json")

# ---------------------- Carga base: librerías si existen ----------------------
def cargar_desde_librerias():
    try:
        import periodictable as pt
        tabla = {}
        for Z in range(1, 119):
            el = pt.elements[Z]
            if el is None:
                continue
            try:
                masa = float(el.mass)
            except Exception:
                masa = float(getattr(el, "standard_atomic_weight", el.mass))
            nombre = str(el.name) if getattr(el, "name", None) else el.symbol
            tabla[el.symbol] = (nombre, masa)
        return tabla, "periodictable"
    except Exception:
        pass

    try:
        from mendeleev import element
        tabla = {}
        for Z in range(1, 119):
            el = element(Z)
            nombre = el.name or el.symbol
            masa = float(el.atomic_weight)
            tabla[el.symbol] = (nombre, masa)
        return tabla, "mendeleev"
    except Exception:
        pass

    return None, None

# -------- Respaldo local básico por si la importación tiene un error ------
TABLA_LOCAL_BASICA = {
    "H": ("Hidrógeno", 1.008), "He": ("Helio", 4.0026), "Li": ("Litio", 6.94),
    "Be": ("Berilio", 9.0122), "B": ("Boro", 10.81), "C": ("Carbono", 12.011),
    "N": ("Nitrógeno", 14.007), "O": ("Oxígeno", 15.999), "F": ("Flúor", 18.998),
    "Ne": ("Neón", 20.180), "Na": ("Sodio", 22.990), "Mg": ("Magnesio", 24.305),
    "Al": ("Aluminio", 26.982), "Si": ("Silicio", 28.085), "P": ("Fósforo", 30.974),
    "S": ("Azufre", 32.06), "Cl": ("Cloro", 35.45), "Ar": ("Argón", 39.948),
    "K": ("Potasio", 39.098), "Ca": ("Calcio", 40.078), "Sc": ("Escandio", 44.956),  # añadido
    "Ti": ("Titanio", 47.867),  "V": ("Vanadio", 50.942),  "Cr": ("Cromo", 51.996),
    "Mn": ("Manganeso", 54.938), "Fe": ("Hierro", 55.845), "Co": ("Cobalto", 58.933),
    "Ni": ("Níquel", 58.693), "Cu": ("Cobre", 63.546), "Zn": ("Zinc", 65.38),
    "Ag": ("Plata", 107.8682), "I": ("Yodo", 126.904), "Au": ("Oro", 196.967),
    "Hg": ("Mercurio", 200.59), "Pb": ("Plomo", 207.2)
}

def cargar_custom():
    if RUTA_CUSTOM.exists():
        try:
            data = json.loads(RUTA_CUSTOM.read_text(encoding="utf-8"))
            # Normaliza a (nombre, masa)
            tabla = {k: (v[0], float(v[1])) for k, v in data.items()}
            return tabla
        except Exception:
            pass
    return {}

def guardar_custom(tabla_custom):
    try:
        RUTA_CUSTOM.write_text(
            json.dumps(tabla_custom, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception:
        pass

# ---------------------- Construcción final de tabla ----------------------
def construir_tabla_periodica():
    tabla, fuente = cargar_desde_librerias()
    if tabla is None:
        # sin librerías → usa local básica
        tabla = dict(TABLA_LOCAL_BASICA)
        fuente = "local"
    # fusiona con custom (lo añadido por el usuario)
    custom = cargar_custom()
    tabla.update(custom)  # lo personalizado sobrescribe
    return tabla, fuente

TABLA, FUENTE = construir_tabla_periodica()

# ---------------------- Parser químico ----------------------
_NUM = re.compile(r'\d+')
_ELEM = re.compile(r'[A-Z][a-z]?')

def leer_num(s, i):
    m = _NUM.match(s, i)
    if m:
        return int(m.group()), m.end()
    return 1, i

def leer_elemento(s, i):
    m = _ELEM.match(s, i)
    if not m:
        raise ValueError(f"Se esperaba un elemento en la posición {i+1}.")
    elem = m.group()
    if elem not in TABLA:
        # Si no existe, permitir agregarlo
        print(f"⚠️ Elemento '{elem}' no encontrado (fuente: {FUENTE}).")
        if input(f"¿Deseas agregar '{elem}' ahora? (SI/NO): ").strip().upper() == "S":
            nombre = input(f"Nombre para {elem}: ").strip() or elem
            while True:
                try:
                    masa = float(input(f"Masa atómica de {elem} (g/mol): ").strip())
                    break
                except ValueError:
                    print("Ingresa un número válido (usa punto decimal).")
            # Guarda en custom y actualiza TABLA en caliente
            custom = cargar_custom()
            custom[elem] = (nombre, masa)
            guardar_custom(custom)
            TABLA[elem] = (nombre, masa)
            print(f"✅ '{elem}' agregado y guardado en {RUTA_CUSTOM}.")
        else:
            raise KeyError(f"Elemento '{elem}' no encontrado.")
    i = m.end()
    mult, i = leer_num(s, i)
    masa = TABLA[elem][1] * mult
    return masa, i

def parse_grupo(s, i=0):
    total = 0.0
    n = len(s)
    while i < n:
        c = s[i]
        if c == ')':
            i += 1
            mult, i = leer_num(s, i)
            return total * mult, i
        if c.isdigit():
            coef, i = leer_num(s, i)
            if i >= n:
                raise ValueError("Coeficiente al final sin término que multiplicar.")
            if s[i] == '(':
                masa_sub, i = parse_grupo(s, i + 1)
            else:
                masa_sub, i = leer_elemento(s, i)
            total += coef * masa_sub
            continue
        if c == '(':
            masa_sub, i = parse_grupo(s, i + 1)
            total += masa_sub
            continue
        if c.isalpha():
            masa_el, i = leer_elemento(s, i)
            total += masa_el
            continue
        break
    return total, i

def masa_de_segmento(segmento):
    segmento = segmento.strip()
    if not segmento:
        return 0.0
    i = 0
    coef_global, i = leer_num(segmento, 0)
    masa, i = parse_grupo(segmento, i)
    if i != len(segmento):
        resto = segmento[i:]
        raise ValueError(f"Entrada no válida cerca de: '{resto}'")
    return coef_global * masa

def calcular_masa_molecular(formula):
    partes = re.split(r'[·\.]', formula.replace(' ', ''))
    masa_total = 0.0
    for parte in partes:
        if parte:
            masa_total += masa_de_segmento(parte)
    return masa_total

# ---------------------- Programa principal ----------------------
def calcular():
    formula = entrada_formula.get().strip()
    if not formula:
        messagebox.showwarning("Advertencia", "Por favor ingresa una fórmula química.")
        return
    try:
        resultado = calcular_masa_molecular(formula)
        etiqueta_resultado.config(
            text=f"La masa molecular de {formula} es: {resultado:.4f} g/mol"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

ventana = tk.Tk()
ventana.title("Calculadora de masa molecular")
ventana.geometry("420x250")

tk.Label(ventana, text="Introduce la fórmula química:", font=("Calibri", 16)).pack(pady=10)
entrada_formula = tk.Entry(ventana, width=30, font=("Calibri", 16))
entrada_formula.pack()

tk.Button(
        ventana,
        text="Calcular",
        command=calcular,
        font=("Calibri", 16),
        bg="#040239",
        fg="white"
    ).pack(pady=10)
etiqueta_resultado = tk.Label(ventana, text="", font=("Calibri", 14))
etiqueta_resultado.pack(pady=10)
ventana.mainloop()