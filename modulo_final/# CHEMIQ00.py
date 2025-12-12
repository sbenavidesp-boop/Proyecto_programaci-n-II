# CHEMIQ00
# tabla periódica completa, historial y diagrama de flujo interactivo.

import tkinter as tk
from tkinter import messagebox, ttk
import re
import json
from pathlib import Path
from datetime import datetime
import subprocess, sys

# ---------------------- Instalación automática ----------------------
def asegurar_libreria(nombre):
    """Instala el paquete si no está disponible."""
    try:
        __import__(nombre)
    except ImportError:
        print(f"📦 Instalando {nombre} automáticamente...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", nombre])

# Librerías externas básicas
try:
    import periodictable
except ImportError:
    try:
        asegurar_libreria("periodictable")
        import periodictable
    except Exception:
        asegurar_libreria("mendeleev")

# ---------- Pillow ----------
_HAVE_PIL = True
try:
    from PIL import Image, ImageTk
except Exception:
    _HAVE_PIL = False

# ---------------------- Librerías NUEVAS (MÓDULO 3) ----------------------
asegurar_libreria("pandas")
asegurar_libreria("matplotlib")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ---------------------- Rutas ----------------------
HIST_PATH = Path("historial.json")

# ---------------------- Funciones de logo ----------------------
LOGO_NOMBRES = ["LOGO-removebg-preview.png"]

def resolver_ruta_logo():
    bases = [
        Path.cwd(),
        Path.home() / "_CHEMIQ",
    ]
    for base in bases:
        for nombre in LOGO_NOMBRES:
            ruta = base / nombre
            if ruta.exists():
                return ruta
    return None

def cargar_logo(max_width=420, max_height=180):
    ruta = resolver_ruta_logo()
    if ruta is None:
        return None
    if _HAVE_PIL:
        try:
            img = Image.open(ruta)
            w, h = img.size
            factor = min(max_width / w, max_height / h, 1.0)
            if factor < 1.0:
                img = img.resize((int(w * factor), int(h * factor)))
            return ImageTk.PhotoImage(img)
        except Exception:
            pass
    try:
        pimg = tk.PhotoImage(file=str(ruta))
        fw = max(1, int(pimg.width() / max_width))
        fh = max(1, int(pimg.height() / max_height))
        f = max(fw, fh)
        if f > 1:
            pimg = pimg.subsample(f, f)
        return pimg
    except Exception:
        return None

# ---------------------- Tabla periódica ----------------------
TABLA_LOCAL = {
    "H": ("Hidrógeno", 1.008), "He": ("Helio", 4.0026), "Li": ("Litio", 6.94),
    "Be": ("Berilio", 9.0122), "B": ("Boro", 10.81), "C": ("Carbono", 12.011),
    "N": ("Nitrógeno", 14.007), "O": ("Oxígeno", 15.999), "F": ("Flúor", 18.998),
    "Na": ("Sodio", 22.990), "Mg": ("Magnesio", 24.305), "Al": ("Aluminio", 26.982),
    "Si": ("Silicio", 28.085), "P": ("Fósforo", 30.974), "S": ("Azufre", 32.06),
    "Cl": ("Cloro", 35.45), "K": ("Potasio", 39.098), "Ca": ("Calcio", 40.078),
    "Fe": ("Hierro", 55.845), "Cu": ("Cobre", 63.546), "Zn": ("Zinc", 65.38),
    "Ag": ("Plata", 107.8682), "I": ("Yodo", 126.904), "Au": ("Oro", 196.967),
    "Hg": ("Mercurio", 200.59), "Pb": ("Plomo", 207.2)
}

def construir_tabla_periodica(base_local: dict):
    try:
        import periodictable as pt
        tabla = {}
        for Z in range(1, 119):
            el = pt.elements[Z]
            if el is None:
                continue
            masa = float(getattr(el, "mass", getattr(el, "standard_atomic_weight", 0)))
            tabla[el.symbol] = (el.name, masa)
        return tabla, "periodictable"
    except Exception:
        pass
    try:
        from mendeleev import element
        tabla = {}
        for Z in range(1, 119):
            el = element(Z)
            tabla[el.symbol] = (el.name or el.symbol, float(el.atomic_weight))
        return tabla, "mendeleev"
    except Exception:
        pass
    return dict(base_local), "local"

TABLA, FUENTE_TABLA = construir_tabla_periodica(TABLA_LOCAL)

# ---------------------- Parser químico ----------------------
_NUM = re.compile(r'\d+')
_ELEM = re.compile(r'[A-Z][a-z]?')

def leer_num(s, i):
    m = _NUM.match(s, i)
    return (int(m.group()), m.end()) if m else (1, i)

def leer_elemento(s, i):
    m = _ELEM.match(s, i)
    if not m:
        raise ValueError(f"Se esperaba un elemento en la posición {i+1}.")
    elem = m.group()
    if elem not in TABLA:
        raise KeyError(f"Elemento '{elem}' no encontrado (fuente: {FUENTE_TABLA}).")
    i = m.end()
    mult, i = leer_num(s, i)
    masa = TABLA[elem][1] * mult
    return masa, i

def parse_grupo(s, i=0):
    total = 0.0
    n = len(s)
    while i < n:
        c = s[i]
        if c in ')]}':
            i += 1
            mult, i = leer_num(s, i)
            return total * mult, i
        if c.isdigit():
            coef, i = leer_num(s, i)
            masa_sub, i = (parse_grupo(s, i + 1) if s[i] in '([{' else leer_elemento(s, i))
            total += coef * masa_sub
            continue
        if c in '([{':
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
    coef_global, i = leer_num(segmento, 0)
    masa, i = parse_grupo(segmento, i)
    if i != len(segmento):
        raise ValueError(f"Entrada no válida cerca de: '{segmento[i:]}'")
    return coef_global * masa

def calcular_masa_molecular(formula):
    partes = re.split(r'[·\.]', formula.replace(' ', ''))
    return sum(masa_de_segmento(p) for p in partes if p)

# ---------------------- Historial ----------------------
def cargar_historial():
    if HIST_PATH.exists():
        try:
            return json.loads(HIST_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def guardar_historial(lista):
    HIST_PATH.write_text(json.dumps(lista, ensure_ascii=False, indent=2), encoding="utf-8")

def agregar_a_historial(formula, masa):
    lista = cargar_historial()
    lista.append({
        "formula": formula,
        "masa": round(float(masa), 6),
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })
    lista = sorted(lista, key=lambda x: x["timestamp"], reverse=True)
    guardar_historial(lista)

# ---------------------- MÓDULO 3: FUNCIÓN ORIGINAL (ya no se usa directamente) ----------------------
def analizar_historial():
    """Versión original que mostraba las 3 gráficas seguidas (la dejamos por si la necesitas)."""
    lista = cargar_historial()

    if not lista:
        messagebox.showinfo("Análisis", "No hay datos en el historial todavía.")
        return

    df = pd.DataFrame(lista)

    # ----- GRÁFICO 1: Histograma -----
    df["tipo_crudo"] = df["masa"].apply(lambda m: clasificar_compuesto(m)[1])

    df["tipo_simple"] = df["tipo_crudo"].apply(
        lambda t: "Inorgánico" if "inorgánico" in t.lower() else "Orgánico"
    )

    conteo = df["tipo_simple"].value_counts()

    plt.figure(figsize=(6, 4))

    colores_tipo = {
        "Inorgánico": "#0b3d91",
        "Orgánico": "#5a2ea6",
    }
    colores_barras = [colores_tipo.get(idx, "#00838f") for idx in conteo.index]

    ax = conteo.plot(kind="bar", color=colores_barras)

    plt.title("Cantidad de compuestos orgánicos e inorgánicos medidos")
    plt.xlabel("Tipo de compuesto")
    plt.ylabel("Cantidad de mediciones")
    plt.grid(True, axis="y", alpha=0.3)

    ax.set_ylim(0, conteo.max() * 1.25)

    for cont in ax.containers:
        ax.bar_label(cont, fmt="%d", padding=3)

    plt.tight_layout()
    plt.show()

    # ----- GRÁFICO 2: Top fórmulas -----
    top = df["formula"].value_counts().head(5)

    plt.figure(figsize=(8, 5))

    colores_formulas = ["#0b3d91", "#026a9f", "#5a2ea6", "#00838f", "#b71c1c"]
    colores_top = colores_formulas[:len(top)]

    ax2 = top.plot(kind="bar", color=colores_top)
    ax2.set_ylim(0, top.max() * 1.30)

    plt.title("Top 5 fórmulas más calculadas")
    plt.xlabel("Fórmula")
    plt.ylabel("Cantidad")
    plt.grid(True, axis="y", alpha=0.3)
    plt.xticks(rotation=45, ha="right")

    for cont in ax2.containers:
        ax2.bar_label(cont, fmt="%d", padding=3)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.show()

    # ----- GRÁFICO 3: Línea temporal -----
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    plt.figure(figsize=(9, 4))
    ax = plt.gca()

    ax.plot(df["timestamp"], df["masa"], marker="o")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))

    plt.xticks(rotation=0, ha="center")

    plt.title("Masa molecular calculada a lo largo del tiempo")
    plt.xlabel("Fecha y hora")
    plt.ylabel("Masa (g/mol)")

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.22)

    plt.grid(True, alpha=0.3)
    plt.show()

# ---------------------- NUEVO: MENÚ DE ANÁLISIS Y GRÁFICAS INDIVIDUALES ----------------------
def grafico_histograma():
    lista = cargar_historial()
    if not lista:
        messagebox.showinfo("Análisis", "No hay datos en el historial todavía.")
        return

    df = pd.DataFrame(lista)
    df["tipo_crudo"] = df["masa"].apply(lambda m: clasificar_compuesto(m)[1])
    df["tipo_simple"] = df["tipo_crudo"].apply(
        lambda t: "Inorgánico" if "inorgánico" in t.lower() else "Orgánico"
    )

    conteo = df["tipo_simple"].value_counts()

    plt.figure(figsize=(6, 4))
    colores = {
        "Inorgánico": "#0b3d91",
        "Orgánico": "#5a2ea6"
    }
    colores_barras = [colores.get(idx, "#00838f") for idx in conteo.index]

    ax = conteo.plot(kind="bar", color=colores_barras)
    ax.set_ylim(0, conteo.max() * 1.30)

    for cont in ax.containers:
        ax.bar_label(cont, fmt="%d", padding=3)

    plt.title("Cantidad de compuestos orgánicos e inorgánicos")
    plt.xlabel("Tipo")
    plt.ylabel("Cantidad")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

def grafico_top5():
    lista = cargar_historial()
    if not lista:
        messagebox.showinfo("Análisis", "No hay datos en el historial todavía.")
        return

    df = pd.DataFrame(lista)
    top = df["formula"].value_counts().head(5)

    plt.figure(figsize=(8, 5))
    colores = ["#0b3d91", "#026a9f", "#5a2ea6", "#00838f", "#b71c1c"]
    colores = colores[:len(top)]

    ax = top.plot(kind="bar", color=colores)
    ax.set_ylim(0, top.max() * 1.30)

    for cont in ax.containers:
        ax.bar_label(cont, fmt="%d", padding=3)

    plt.title("Top 5 fórmulas más calculadas")
    plt.xlabel("Fórmula")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.show()

def grafico_linea():
    lista = cargar_historial()
    if not lista:
        messagebox.showinfo("Análisis", "No hay datos en el historial todavía.")
        return

    df = pd.DataFrame(lista)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    plt.figure(figsize=(9, 4))
    ax = plt.gca()
    ax.plot(df["timestamp"], df["masa"], marker="o")

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    plt.xticks(rotation=0, ha="center")

    plt.title("Masa molecular a lo largo del tiempo")
    plt.xlabel("Fecha")
    plt.ylabel("Masa (g/mol)")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.22)
    plt.show()

def menu_analisis():
    win = tk.Toplevel()
    win.title("Análisis – CHEMIQ")
    win.geometry("360x260")
    win.configure(bg="#ffffff")

    tk.Label(
        win,
        text="Seleccione el análisis que desea ver:",
        bg="#ffffff",
        font=("Segoe UI", 12, "bold"),
        fg="#222"
    ).pack(pady=12)

    tk.Button(
        win, text="📊 Histograma",
        font=("Segoe UI", 11),
        bg="#1565c0", fg="white",
        command=lambda: (win.destroy(), grafico_histograma())
    ).pack(pady=6, ipadx=10, ipady=4)

    tk.Button(
        win, text="🧪 Top 5 fórmulas",
        font=("Segoe UI", 11),
        bg="#7b1fa2", fg="white",
        command=lambda: (win.destroy(), grafico_top5())
    ).pack(pady=6, ipadx=10, ipady=4)

    tk.Button(
        win, text="📈 Línea temporal",
        font=("Segoe UI", 11),
        bg="#00838f", fg="white",
        command=lambda: (win.destroy(), grafico_linea())
    ).pack(pady=6, ipadx=10, ipady=4)

    tk.Button(
        win, text="🔙 Regresar",
        font=("Segoe UI", 11),
        bg="#b71c1c", fg="white",
        command=win.destroy
    ).pack(pady=10, ipadx=10, ipady=4)

# ---------------------- MINI IA ----------------------
def clasificar_compuesto(masa):
    """
    Mini IA: clasificación simple basada en reglas + comparación con historial.
    Produce un análisis más natural y profesional.
    """

    # ----- 1. Tipo de masa -----
    if masa < 50:
        categoria = "Masa baja (compuesto ligero)"
    elif masa < 150:
        categoria = "Masa media"
    else:
        categoria = "Masa alta (compuesto pesado)"

    # ----- 2. Tipo probable -----
    tipo = "Compuesto inorgánico" if masa < 200 else "Compuesto orgánico complejo"

    # ----- 3. Comparación con historial -----
    lista = cargar_historial()
    masas_previas = [item["masa"] for item in lista] if lista else []

    if masas_previas:
        menores_iguales = sum(1 for m in masas_previas if m <= masa)
        porcentaje = round((menores_iguales / len(masas_previas)) * 100, 1)

        if 30 <= porcentaje <= 70:
            nivel = "Intermedio"
        elif 10 <= porcentaje <= 90:
            nivel = "Completo"
        else:
            nivel = "Básico"

        explicacion = (
            f"Esta masa es mayor o igual que el {porcentaje}% de los "
            f"compuestos calculados por CHEMIQ."
        )
    else:
        nivel = "Inicial"
        explicacion = "Aún no hay suficientes datos previos en CHEMIQ para contextualizar este resultado."

    return categoria, tipo, nivel, explicacion

# ---------------------- FUNCIONES GUI ----------------------
def dibujar_degradado(canvas, width, height, start=(10, 45, 180), end=(120, 40, 160)):
    for i in range(height):
        r = int(start[0] + (end[0] - start[0]) * i / height)
        g = int(start[1] + (end[1] - start[1]) * i / height)
        b = int(start[2] + (end[2] - start[2]) * i / height)
        canvas.create_line(0, i, width, i, fill=f"#{r:02x}{g:02x}{b:02x}", tags="bg")

def mostrar_ayuda():
    ejemplos = (
        "Ejemplos válidos:\n"
        "• H2O → Agua\n"
        "• (NH4)2SO4 → Sulfato de amonio\n"
        "• Fe2(SO4)3·9H2O → Sulfato férrico nonahidratado\n"
        "• K4[Fe(CN)6] → Ferricianuro de potasio\n"
        "Soporta (), [], {}, y punto o punto medio para hidratados."
    )
    messagebox.showinfo("Ayuda - Ejemplos de uso", ejemplos)

def abrir_historial(ventana):
    win = tk.Toplevel(ventana)
    win.title("Historial de cálculos")
    win.geometry("520x380")
    win.configure(bg="#f6f6fb")

    cols = ("formula", "masa", "momento")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=12)

    for col, txt in zip(cols, ["Fórmula", "Masa (g/mol)", "Fecha/Hora"]):
        tree.heading(col, text=txt)

    tree.pack(padx=12, pady=12, fill="both", expand=True)

    for item in cargar_historial():
        tree.insert("", "end",
                    values=(item["formula"], f'{item["masa"]:.4f}', item["timestamp"].replace("T", " ")))

    cont = tk.Frame(win, bg="#f6f6fb")
    cont.pack(pady=6)

    def limpiar():
        if messagebox.askyesno("Confirmar", "¿Deseas borrar todo el historial?"):
            guardar_historial([])
            for i in tree.get_children():
                tree.delete(i)

    tk.Button(cont, text="🗑️ Limpiar historial", command=limpiar,
              bg="#c62828", fg="white").grid(row=0, column=0, padx=6)

    tk.Button(cont, text="Cerrar", command=win.destroy,
              bg="#444", fg="white").grid(row=0, column=1, padx=6)

def calcular(ventana, entrada_formula, etiqueta_resultado):
    formula = entrada_formula.get().strip()
    if not formula:
        messagebox.showwarning("Advertencia", "Por favor ingresa una fórmula química.")
        return

    try:
        resultado = calcular_masa_molecular(formula)

        categoria, tipo, confianza, explicacion = clasificar_compuesto(resultado)

        etiqueta_resultado.config(
            text=(
                f"Masa molecular de {formula}: {resultado:.4f} g/mol\n\n"
                f"🔎 Análisis automático CHEMIQ-IA:\n"
                f"• Tipo de masa: {categoria}\n"
                f"• Tipo estimado: {tipo}\n"
                f"• Alcance del análisis: {confianza}\n"
                f"• {explicacion}"
            )
        )

        ventana.clipboard_clear()
        ventana.clipboard_append(f"{resultado:.4f}")

        agregar_a_historial(formula, resultado)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

# ---------------------- Diagrama de flujo ----------------------
def abrir_flujo_datos():
    win = tk.Toplevel()
    win.title("Flujo de Datos - CHEMIQ")
    win.geometry("640x420")
    win.config(bg="#0d0630")

    canvas = tk.Canvas(win, bg="#0d0630", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    nodos = [
        ("👩‍🔬 Usuario", 320, 60, "#5a2ea6"),
        ("📥 Entrada fórmula", 320, 140, "#283593"),
        ("⚙️ Cálculo", 320, 220, "#1565c0"),
        ("📤 Resultado", 320, 300, "#0277bd"),
        ("💾 Historial", 320, 380, "#00838f"),
    ]

    circulos, textos = [], []
    for texto, x, y, color in nodos:
        c = canvas.create_oval(x-100, y-30, x+100, y+30,
                               fill=color, width=0, state="hidden")
        t = canvas.create_text(x, y, text=texto, fill="white",
                               font=("Segoe UI", 12, "bold"), state="hidden")
        circulos.append(c)
        textos.append(t)

    def animar(i=0):
        if i >= len(nodos):
            return
        canvas.itemconfigure(circulos[i], state="normal")
        canvas.itemconfigure(textos[i], state="normal")

        if i < len(nodos)-1:
            x1, y1 = nodos[i][1], nodos[i][2] + 30
            x2, y2 = nodos[i+1][1], nodos[i+1][2] - 30
            flecha = canvas.create_line(x1, y1, x2, y2,
                                        arrow=tk.LAST, width=3,
                                        fill="#b3e5fc",
                                        state="hidden")

            def mostrar():
                canvas.itemconfigure(flecha, state="normal")
                canvas.after(500, lambda: animar(i + 1))

            canvas.after(400, mostrar)

        else:
            canvas.after(500, lambda: canvas.create_text(
                320, 30, text="💡 Flujo completo de datos",
                fill="white", font=("Segoe UI", 14, "bold")
            ))

    animar()

    tk.Button(win, text="Cerrar", command=win.destroy,
              bg="#6a38d9", fg="white").place(relx=1.0, rely=0.0, x=-12, y=10, anchor="ne")

# ---------------------- Ventana principal ----------------------
def construir_contenido(frame, ventana):
    tk.Label(frame, text="Calculadora de masa molecular", bg="#ffffff",
             font=("Segoe UI", 14, "bold"), fg="#222").pack(pady=(10, 6))

    tk.Label(frame, text=f"Fuente de tabla: {FUENTE_TABLA}", bg="#ffffff",
             font=("Segoe UI", 9, "italic"), fg="#555").pack(pady=(0, 6))

    tk.Label(frame, text="Ingresa la fórmula química:", bg="#ffffff",
             font=("Segoe UI", 11), fg="#333").pack(pady=(6, 4))

    entrada_formula = tk.Entry(frame, width=32, font=("Segoe UI", 12),
                               relief="solid", bd=1)
    entrada_formula.pack(pady=(0, 10))
    entrada_formula.focus_set()

    cont = tk.Frame(frame, bg="#ffffff")
    cont.pack(pady=6)

    tk.Button(cont, text="Calcular",
              command=lambda: calcular(ventana, entrada_formula, etiqueta_resultado),
              font=("Segoe UI", 11), bg="#0b3d91", fg="white",
              padx=12, pady=6).grid(row=0, column=0, padx=6)

    tk.Button(cont, text="Ayuda", command=mostrar_ayuda,
              font=("Segoe UI", 11), bg="#026a9f", fg="white",
              padx=12, pady=6).grid(row=0, column=1, padx=6)

    tk.Button(cont, text="Historial",
              command=lambda: abrir_historial(ventana),
              font=("Segoe UI", 11), bg="#5a2ea6", fg="white",
              padx=12, pady=6).grid(row=0, column=2, padx=6)

    tk.Button(cont, text="Flujo de Datos",
              command=abrir_flujo_datos,
              font=("Segoe UI", 11), bg="#00838f", fg="white",
              padx=12, pady=6).grid(row=0, column=3, padx=6)

    # ---------------------- BOTÓN ANÁLISIS (NUEVO MENÚ) ----------------------
    tk.Button(cont, text="Análisis",
              command=menu_analisis,
              font=("Segoe UI", 11), bg="#b71c1c", fg="white",
              padx=12, pady=6).grid(row=0, column=4, padx=6)

    global etiqueta_resultado
    etiqueta_resultado = tk.Label(
        frame,
        text="",
        bg="#ffffff",
        font=("Segoe UI", 12),
        fg="#111",
        wraplength=480,   # ancho para que el texto no se salga
        justify="center"
    )
    etiqueta_resultado.pack(pady=(20, 20))

def crear_ventana():
    ventana = tk.Tk()
    ventana.title("CHEMIQ – Calculadora de Masa Molecular")
    ventana.geometry("620x580")
    ventana.minsize(600, 580)

    canvas = tk.Canvas(ventana, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    ventana._logo_img = cargar_logo()

    frame = tk.Frame(canvas, bg="#ffffff",
                     highlightbackground="#ccc", highlightthickness=1)
    ventana._card_frame = frame
    construir_contenido(frame, ventana)

    def on_resize(event):
        canvas.delete("bg")
        w, h = event.width, event.height

        dibujar_degradado(canvas, w, h)

        if ventana._logo_img:
            canvas.create_image(w // 2, 90, image=ventana._logo_img, tags="logo")
        else:
            canvas.create_text(w // 2, 90, text="CHEMIQ",
                               fill="white", font=("Segoe UI", 24, "bold"),
                               tags="logo")

        card_w, card_h = 520, 420
        x, y = (w - card_w) // 2, 180

        if not hasattr(ventana, "_frame_id"):
            ventana._frame_id = canvas.create_window(
                x + card_w // 2, y + card_h // 2,
                window=ventana._card_frame, width=card_w, height=card_h
            )
        else:
            canvas.coords(ventana._frame_id, x + card_w // 2, y + card_h // 2)

    canvas.bind("<Configure>", on_resize)
    return ventana

# ---------------------- Ejecutar ----------------------
if __name__ == "__main__":
    app = crear_ventana()
    app.mainloop()
