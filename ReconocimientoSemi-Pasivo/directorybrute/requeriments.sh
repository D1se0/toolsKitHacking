#!/bin/bash

# Verificar si se ejecuta como root
if [ "$(id -u)" != "0" ]; then
    echo "Este script debe ser ejecutado como root. Por favor, usa 'sudo' o inicia sesión como root."
    exit 1
fi

# Instalación de los requisitos
echo "Instalando requerimientos..."
pip3 install requests colorama tqdm

# Copiar el script a /usr/bin si existe
if [ -f directorybrute.py ]; then
    echo "Copiando script a /usr/bin..."
    cp directorybrute.py /usr/bin/directorybrute
    chmod +x /usr/bin/directorybrute
else
    echo "No se encontró el archivo directorybrute.py en el directorio actual. Asegúrate de que el archivo esté presente y ejecuta el script nuevamente."
    exit 1
fi

# Ejecutar el script dentro del entorno virtual
echo "Ejecutando herramienta"
directorybrute -h

echo "Hecho. Ahora puedes usar 'directorybrute' como comando en cualquier parte del sistema."
