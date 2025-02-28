#!/bin/bash

# Función para instalar SEToolkit desde los repositorios
instalar_setoolkit() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando Social-Engineer Toolkit (SEToolkit)..."
    sudo apt install -y set

    if [ $? -eq 0 ]; then
        echo "[+] SEToolkit se ha instalado correctamente."
    else
        echo "[!] Hubo un error durante la instalación de SEToolkit."
        exit 1
    fi
}

# Ejecutar la función
instalar_setoolkit
