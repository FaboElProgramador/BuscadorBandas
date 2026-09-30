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

La aplicacion permite introducir una palabra clave y una URL por linea. Selenium abre las paginas en segundo plano y muestra si encuentra la palabra buscada.