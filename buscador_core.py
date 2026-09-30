import unicodedata

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import Request, urlopen


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(
        caracter for caracter in texto
        if not unicodedata.combining(caracter)
    )


def descargar_html(url):
    try:
        solicitud = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(solicitud, timeout=20) as respuesta:
            codificacion = respuesta.headers.get_content_charset() or "utf-8"
            return respuesta.read().decode(codificacion, errors="replace")
    except Exception:
        return ""


def buscar_paginas(palabra, urls, informar):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = "none"

    try:
        navegador = webdriver.Chrome(options=chrome_options)
        navegador.set_page_load_timeout(20)
    except WebDriverException as error:
        informar(f"⚠️ Error iniciando el navegador: {error}\n")
        return

    try:
        total_urls = len(urls)
        artista = normalizar_texto(palabra)
        for indice, url in enumerate(urls, start=1):
            informar(f"Fuente {indice}/{total_urls}: {url}\n")
            try:
                contenido_estatico = descargar_html(url)
                if contenido_estatico and artista in normalizar_texto(contenido_estatico):
                    informar(f"✅ Encontrado en: {url}\n")
                    continue

                try:
                    navegador.get(url)
                except TimeoutException:
                    informar("⚠️ La página tardó demasiado; se analizará el contenido disponible.\n")

                try:
                    WebDriverWait(navegador, 15).until(
                        lambda driver: artista in normalizar_texto(
                            driver.find_element("tag name", "body").text
                        )
                    )
                except TimeoutException:
                    informar("⚠️ El artista no apareció durante la carga; se analizará el contenido disponible.\n")

                contenido_visible = navegador.find_element("tag name", "body").text
                contenido = normalizar_texto(f"{contenido_visible} {navegador.page_source}")
                resultado = "✅ Encontrado" if artista in contenido else "❌ No encontrado"
                informar(f"{resultado} en: {url}\n")
            except Exception as error:
                informar(f"⚠️ Error al acceder {url}: {error}\n")
    finally:
        navegador.quit()