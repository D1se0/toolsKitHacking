#!/bin/bash

# Función para instalar Bettercap
instalar_bettercap() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando dependencias necesarias..."
    sudo apt install -y build-essential libpcap-dev net-tools

    echo "[+] Instalando Bettercap..."
    sudo apt install -y bettercap

    if [ $? -eq 0 ]; then
        echo "[+] Bettercap se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar Bettercap."
    fi
}

# Ejecutar la función
instalar_bettercap
