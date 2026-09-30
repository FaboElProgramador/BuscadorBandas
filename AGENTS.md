# AGENTS.md

## Visión general
Este repositorio contiene una pequeña aplicación de escritorio en Python para buscar artistas o palabras clave en varias páginas web, incluyendo sitios que cargan contenido con JavaScript.

El proyecto está dividido en dos partes principales:

- `buscador_core.py`: contiene la lógica de búsqueda, normalización de texto y acceso a páginas con Selenium + `urllib`.
- `buscador_de_bandnas.pyw`: incluye la interfaz gráfica en Tkinter y el flujo principal de la aplicación.

Antes de cambiar la lógica del programa, revisa también [README.md](README.md).

## Cómo arrancar la app

### Requisitos
- Python 3.11+
- Google Chrome
- Selenium

### Instalación

```powershell
pip install selenium
```

### Ejecución

```powershell
python .\buscador_de_bandnas.pyw
```

## Convenciones del proyecto
- Mantén separadas la lógica de scraping y la interfaz gráfica.
- La GUI no debe incluir lógica de scraping compleja ni validación de páginas.
- `fuentes.txt` usa una URL por línea y admite comentarios con `#` al inicio.
- Las URLs válidas deben usar `http` o `https` y contener un dominio.
- El proyecto está escrito en español y los mensajes de usuario deben mantenerse en ese idioma.
- No agregues nuevas dependencias sin documentarlas y validar el comportamiento.

## Patrones importantes para agentes
- Si cambias `normalizar_texto()`, revisa todo su uso porque afecta comparaciones y detección de coincidencias.
- Si tocas Selenium, considera tanto el contenido estático descargado con `urlopen` como el contenido dinámico renderizado por Chrome.
- Si agregas o cambias URLs en `fuentes.txt`, conserva el formato actual para no romper la carga automática.
- La app usa `threading.Thread` para no bloquear la interfaz; cualquier cambio en la GUI debe respetar ese patrón.
- La validación de URLs y fechas ya está implementada en la GUI; no la conviertas en lógica duplicada en otras partes.

## Validación sugerida
No hay suite de tests automatizados. La verificación práctica recomendada es:

1. Ejecutar la app con `python .\buscador_de_bandnas.pyw`.
2. Probar con una URL válida y un artista conocido.
3. Confirmar que `fuentes.txt` se carga correctamente y que no aparecen errores de entrada.
4. Revisar que la interfaz sigue respondiendo y que el flujo de búsqueda no bloquea la UI.

## Objetivo de este archivo
Este documento orienta a agentes de IA y colaboradores humanos para entender la estructura del proyecto, sus riesgos principales y las mejores prácticas antes de tocar código.
