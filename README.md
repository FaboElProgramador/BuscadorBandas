# Buscador de bandas

Aplicacion de escritorio para buscar una palabra clave en varias paginas web, incluyendo sitios cuyo contenido se carga con JavaScript.

## Requisitos

- Python 3.11 o superior
- Google Chrome
- Selenium

Instala Selenium con:

```powershell
pip install selenium
```

## Ejecucion

```powershell
python .\buscador_de_bandnas.pyw
```

La aplicacion permite introducir un artista y una URL por linea. Las URLs tambien pueden mantenerse en `fuentes.txt`; usa una línea por URL y antepone `#` a los comentarios. Selenium abre las paginas en segundo plano y muestra si encuentra el artista buscado.

Conviene agregar URLs de carteleras o listados de eventos, como `/shows`. La portada general de una ticketera puede no contener los nombres de los artistas.