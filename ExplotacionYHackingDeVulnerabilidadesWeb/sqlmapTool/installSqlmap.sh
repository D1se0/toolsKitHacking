#!/bin/bash

# Función para instalar sqlmap
instalar_sqlmap() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando sqlmap..."
    sudo apt install -y sqlmap

    if [ $? -eq 0 ]; then
        echo "[+] sqlmap se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar sqlmap."
    fi
}

# Ejecutar la función
instalar_sqlmap
