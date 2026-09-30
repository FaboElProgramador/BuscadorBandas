import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse
import threading

def buscar():
    palabra = entry_palabra.get().strip().lower()
    urls = [url.strip() for url in text_urls.get("1.0", tk.END).splitlines() if url.strip()]
    urls_validas = [url for url in urls if urlparse(url).scheme in ("http", "https") and urlparse(url).netloc]
    urls_invalidas = [url for url in urls if url not in urls_validas]
    resultados.delete("1.0", tk.END)

    if not palabra or not urls:
        messagebox.showwarning("Campos vacíos", "Debes ingresar una palabra clave y al menos una URL.")
        return

    for url in urls_invalidas:
        resultados.insert(tk.END, f"⚠️ URL inválida: {url}\n")

    if not urls_validas:
        messagebox.showwarning("URLs inválidas", "Debes ingresar al menos una URL válida (http o https).")
        return

    btn_buscar.config(state=tk.DISABLED)
    resultados.insert(tk.END, "Buscando...\n\n")
    threading.Thread(target=buscar_en_paginas, args=(palabra, urls_validas), daemon=True).start()

def mostrar_resultado(mensaje):
    resultados.insert(tk.END, mensaje)
    resultados.see(tk.END)

def finalizar_busqueda():
    btn_buscar.config(state=tk.NORMAL)

def buscar_en_paginas(palabra, urls):
    # Configurar navegador sin interfaz gráfica (headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        navegador = webdriver.Chrome(options=chrome_options)
    except WebDriverException as e:
        ventana.after(0, mostrar_resultado, f"⚠️ Error iniciando el navegador: {e}\n")
        ventana.after(0, finalizar_busqueda)
        return

    try:
        for url in urls:
            ventana.after(0, mostrar_resultado, f"Procesando: {url}\n")
            try:
                navegador.get(url)
                WebDriverWait(navegador, 15).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                contenido = navegador.find_element("tag name", "body").text.lower()

                if palabra in contenido:
                    mensaje = f"✅ Encontrado en: {url}\n"
                else:
                    mensaje = f"❌ No encontrado en: {url}\n"
            except Exception as e:
                mensaje = f"⚠️ Error al acceder {url}: {e}\n"

            ventana.after(0, mostrar_resultado, mensaje)
    finally:
        navegador.quit()
        ventana.after(0, finalizar_busqueda)

# GUI igual que antes
ventana = tk.Tk()
ventana.title("Buscador con JS (Selenium)")
ventana.geometry("700x500")

tk.Label(ventana, text="Palabra clave a buscar:").pack()
entry_palabra = tk.Entry(ventana, width=60)
entry_palabra.pack(pady=5)

tk.Label(ventana, text="Páginas web (una por línea):").pack()
text_urls = scrolledtext.ScrolledText(ventana, width=80, height=5)
text_urls.pack(pady=5)
text_urls.insert(tk.END, "https://quilmesrock.enigmatickets.com/\nhttps://www.movistararena.com.ar/")

btn_buscar = tk.Button(ventana, text="Buscar", command=buscar)
btn_buscar.pack(pady=10)

tk.Label(ventana, text="Resultados:").pack()
resultados = scrolledtext.ScrolledText(ventana, width=80, height=15)
resultados.pack(pady=5)

ventana.mainloop()
