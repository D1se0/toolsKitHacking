#!/bin/bash

# Función para actualizar el sistema e instalar Amap
instalar_amap() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando Amap..."
    sudo apt-get install -y amap

    if [ $? -eq 0 ]; then
        echo "[+] Amap se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar Amap."
    fi
}

# Ejecutar la función
instalar_amap
