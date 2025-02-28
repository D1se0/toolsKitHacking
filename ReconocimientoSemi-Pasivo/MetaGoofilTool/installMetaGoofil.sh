#!/bin/bash

# Función para actualizar el sistema e instalar Metagoofil
instalar_metagoofil() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando Metagoofil..."
    sudo apt-get install -y metagoofil

    if [ $? -eq 0 ]; then
        echo "[+] Metagoofil se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar Metagoofil."
    fi
}

# Ejecutar la función
instalar_metagoofil
