#!/bin/bash

# Verificar que se esté ejecutando como root
if [ "$(id -u)" -ne 0 ]; then
    echo "Este script debe ejecutarse como root. Usa sudo o ejecútalo como usuario root."
    exit 1
fi

# Definir la ruta al archivo Python
SCRIPT_PATH="cerbero.py"

# Verificar si el script Python existe
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: No se encontró el script Python en la ruta especificada: $SCRIPT_PATH"
    exit 1
fi

# Instalar dependencias necesarias
echo "Instalando dependencias necesarias..."
apt-get update
apt-get install -y python3-paramiko python3-colorama

# Definir la ruta de instalación en /usr/bin sin la extensión .py
INSTALL_PATH="/usr/bin/cerbero"

# Copiar el script Python a /usr/bin sin la extensión .py
cp "$SCRIPT_PATH" "$INSTALL_PATH"

# Dar permisos de ejecución al archivo en /usr/bin
chmod +x "$INSTALL_PATH"

# Imprimir mensaje de éxito
echo "Cerbero ha sido instalado correctamente en /usr/bin como 'cerbero'"
