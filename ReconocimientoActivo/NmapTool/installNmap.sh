#!/bin/bash

# Función para actualizar el sistema e instalar Nmap
instalar_nmap() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando Nmap..."
    sudo apt-get install -y nmap

    if [ $? -eq 0 ]; then
        echo "[+] Nmap se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar Nmap."
    fi
}

# Ejecutar la función
instalar_nmap
