#!/bin/bash

# Verificar si el script se está ejecutando como root
if [ "$(id -u)" -ne 0 ]; then
    echo "Este script debe ejecutarse como root."
    exit 1
fi

# Nombre del archivo original
ORIGINAL_FILE="suBruteforce.py"

# Verificar si el archivo original existe
if [ ! -f "$ORIGINAL_FILE" ]; then
    echo "El archivo $ORIGINAL_FILE no existe."
    exit 1
fi

# Instalar dependencias necesarias
echo "Instalando dependencias necesarias..."
apt-get update
apt-get install -y python3-pip
pip3 install colorama

# Nombre del archivo destino
DEST_FILE="/usr/bin/suBruteforce"

# Copiar el archivo a /usr/bin/ y renombrarlo
cp $ORIGINAL_FILE $DEST_FILE

# Hacer el archivo ejecutable
chmod +x $DEST_FILE

echo "El script se ha copiado y configurado correctamente en /usr/bin/suBruteforce."
echo "Todas las dependencias se han instalado correctamente."

echo "La herramienta suBruteforce no se puede ejecutar como root, tiene que ser con un usuario normal"
