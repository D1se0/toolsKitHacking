#!/bin/bash

# Actualizar la lista de paquetes
echo "[+] Actualizando la lista de paquetes..."
sudo apt update

# Instalar Maltego
echo "[+] Instalando Maltego..."
sudo apt install -y maltego

# Confirmar que Maltego se ha instalado correctamente
if command -v maltego &> /dev/null; then
    echo "[+] Maltego se ha instalado correctamente."
else
    echo "[!] Hubo un problema al instalar Maltego."
fi

