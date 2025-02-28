# Payload-Generator

Payload-Generator es una herramienta de generación de payloads de red y escucha de conexiones en sistemas remotos. Desarrollada para ambientes de pruebas de penetración, permite crear y ejecutar payloads desde una máquina atacante hacia una máquina víctima usando PowerShell.

## Características

- Generación de payloads personalizados
- Escucha de conexiones en tiempo real
- Interfaz de comandos intuitiva
- Ejecución automatizada de `netcat` para escuchar conexiones

## Capturas de Pantalla

**Payload Generator**

![Inicio de Payload-Generator](https://github.com/ccyl13/Payload-Generator/blob/main/Payload%20Generator.png?raw=true)


## Dependencias

La herramienta está desarrollada en Python 3 y requiere las siguientes dependencias:
- `colorama` para los colores de la interfaz en la línea de comandos
- `netcat` para escuchar conexiones de red en la máquina atacante

Instalación:

```bash
pip install colorama
git clone https://github.com/ccyl13/Payload-Generator.git
cd Payload-Generator
chmod +x payload_generator.py
pip install -r requirements.txt
python3 payload_generator.py

