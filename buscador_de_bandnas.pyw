import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import date, timedelta
from urllib.parse import urlparse
import threading

from buscador_core import buscar_paginas

def buscar():
    palabra = entry_palabra.get().strip().lower()
    ciudad = entry_ciudad.get().strip()
    fecha_desde = entry_fecha_desde.get().strip()
    fecha_hasta = entry_fecha_hasta.get().strip()
    urls = [url.strip() for url in text_urls.get("1.0", tk.END).splitlines() if url.strip()]
    urls_validas = list(dict.fromkeys(
        url for url in urls
        if urlparse(url).scheme in ("http", "https") and urlparse(url).netloc
    ))
    urls_invalidas = [url for url in urls if url not in urls_validas]
    resultados.delete("1.0", tk.END)

    if not palabra or not urls:
        messagebox.showwarning("Campos vacíos", "Debes ingresar un artista y al menos una URL.")
        return

    try:
        fecha_desde_obj = date.fromisoformat(fecha_desde)
        fecha_hasta_obj = date.fromisoformat(fecha_hasta)
    except ValueError:
        messagebox.showwarning("Fechas inválidas", "Usa el formato AAAA-MM-DD.")
        return

    if fecha_desde_obj > fecha_hasta_obj:
        messagebox.showwarning("Rango inválido", "La fecha inicial no puede ser posterior a la fecha final.")
        return

    for url in urls_invalidas:
        resultados.insert(tk.END, f"⚠️ URL inválida: {url}\n")

    if not urls_validas:
        messagebox.showwarning("URLs inválidas", "Debes ingresar al menos una URL válida (http o https).")
        return

    btn_buscar.config(state=tk.DISABLED)
    criterios = f"Artista: {palabra}\nCiudad: {ciudad or 'Todas'}\nFechas: {fecha_desde} a {fecha_hasta}\n\n"
    resultados.insert(tk.END, criterios)
    resultados.insert(tk.END, "Buscando...\n\n")
    threading.Thread(target=buscar_en_paginas, args=(palabra, urls_validas), daemon=True).start()

def mostrar_resultado(mensaje):
    resultados.insert(tk.END, mensaje)
    resultados.see(tk.END)

def finalizar_busqueda():
    btn_buscar.config(state=tk.NORMAL)

def buscar_en_paginas(palabra, urls):
    informar = lambda mensaje: ventana.after(0, mostrar_resultado, mensaje)
    buscar_paginas(palabra, urls, informar)
    ventana.after(0, finalizar_busqueda)

# GUI igual que antes
ventana = tk.Tk()
ventana.title("Buscador con JS (Selenium)")
ventana.geometry("760x650")

tk.Label(ventana, text="Artista:").pack()
entry_palabra = tk.Entry(ventana, width=60)
entry_palabra.pack(pady=5)

tk.Label(ventana, text="Ciudad (opcional):").pack()
entry_ciudad = tk.Entry(ventana, width=60)
entry_ciudad.pack(pady=5)

fecha_predeterminada = date.today()
fecha_final_predeterminada = fecha_predeterminada + timedelta(days=90)

tk.Label(ventana, text="Fechas (formato AAAA-MM-DD):").pack()
frame_fechas = tk.Frame(ventana)
frame_fechas.pack(pady=5)
tk.Label(frame_fechas, text="Desde").grid(row=0, column=0, padx=5)
entry_fecha_desde = tk.Entry(frame_fechas, width=14)
entry_fecha_desde.insert(0, fecha_predeterminada.isoformat())
entry_fecha_desde.grid(row=0, column=1, padx=5)
tk.Label(frame_fechas, text="Hasta").grid(row=0, column=2, padx=5)
entry_fecha_hasta = tk.Entry(frame_fechas, width=14)
entry_fecha_hasta.insert(0, fecha_final_predeterminada.isoformat())
entry_fecha_hasta.grid(row=0, column=3, padx=5)

tk.Label(ventana, text="URLs manuales (una por línea, respaldo temporal):").pack()
text_urls = scrolledtext.ScrolledText(ventana, width=85, height=5)
text_urls.pack(pady=5)
text_urls.insert(tk.END, "https://quilmesrock.enigmatickets.com/\nhttps://www.movistararena.com.ar/")

btn_buscar = tk.Button(ventana, text="Buscar", command=buscar)
btn_buscar.pack(pady=10)

tk.Label(ventana, text="Resultados:").pack()
resultados = scrolledtext.ScrolledText(ventana, width=85, height=15)
resultados.pack(pady=5)

ventana.mainloop()
