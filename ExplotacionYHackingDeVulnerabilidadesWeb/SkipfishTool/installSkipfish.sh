#!/bin/bash

# Función para instalar Skipfish
instalar_skipfish() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando Skipfish..."
    sudo apt install -y skipfish

    if [ $? -eq 0 ]; then
        echo "[+] Skipfish se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar Skipfish."
    fi
}

# Ejecutar la función
instalar_skipfish
