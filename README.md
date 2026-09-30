# Buscador de bandas

Aplicación de escritorio desarrollada en Python para buscar artistas o palabras clave en múltiples páginas web, incluyendo sitios que cargan contenido dinámicamente con JavaScript.

## Descripción

Este proyecto ayuda a detectar si un artista o palabra clave aparece en una serie de URLs configuradas por el usuario. La aplicación combina:

- solicitudes HTTP con `urllib` para contenido estático,
- navegación automatizada con Selenium y Chrome en modo headless,
- una interfaz gráfica con Tkinter para facilitar el uso.

Es útil para validar presencia de artistas en carteleras, listados de eventos o páginas con contenido renderizado por JavaScript.

## Requisitos

- Python 3.11 o superior
- Google Chrome instalado
- Selenium

Instalación recomendada:

```powershell
pip install selenium
```

## Ejecución

```powershell
python .\buscador_de_bandnas.pyw
```

## Cómo funciona

- El usuario ingresa un artista y una o varias URLs.
- La aplicación valida que las URLs sean válidas (`http` o `https`).
- Revisa contenido estático y luego carga cada sitio con Selenium.
- Muestra si el artista buscado aparece o no.
- Las fuentes pueden mantenerse en `fuentes.txt`, con una URL por línea y comentarios con `#`.

## Estructura del proyecto

- `buscador_core.py`: lógica principal de scraping y validación.
- `buscador_de_bandnas.pyw`: interfaz gráfica y flujo principal de la app.
- `fuentes.txt`: archivo con URLs de referencia.
- `README.md`: documentación del proyecto.

## Recomendaciones de uso

- Usa URLs de carteleras, listados de eventos o páginas de shows, no solo la portada general de una ticketera.
- Evita sitios complejos que requieren login o carga heavy con contenido bloqueado por protección.
- Mantén una lista de fuentes bien filtrada para obtener mejores resultados.

## Estado del proyecto

Proyecto personal orientado a automatización básica de búsquedas web con Python y Selenium, pensado para uso práctico y demostración de habilidades en automatización, scraping y aplicaciones de escritorio.