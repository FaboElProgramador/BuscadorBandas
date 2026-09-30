from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def buscar_paginas(palabra, urls, informar):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        navegador = webdriver.Chrome(options=chrome_options)
        navegador.set_page_load_timeout(20)
    except WebDriverException as error:
        informar(f"⚠️ Error iniciando el navegador: {error}\n")
        return

    try:
        for url in urls:
            informar(f"Procesando: {url}\n")
            try:
                navegador.get(url)
                WebDriverWait(navegador, 15).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                contenido = navegador.find_element("tag name", "body").text.lower()
                resultado = "✅ Encontrado" if palabra in contenido else "❌ No encontrado"
                informar(f"{resultado} en: {url}\n")
            except Exception as error:
                informar(f"⚠️ Error al acceder {url}: {error}\n")
    finally:
        navegador.quit()