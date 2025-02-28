#!/bin/bash

# Función para actualizar el sistema e instalar ExifTool
instalar_exiftool() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando ExifTool..."
    sudo apt-get install -y libimage-exiftool-perl

    if [ $? -eq 0 ]; then
        echo "[+] ExifTool se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar ExifTool."
    fi
}

# Ejecutar la función
instalar_exiftool
