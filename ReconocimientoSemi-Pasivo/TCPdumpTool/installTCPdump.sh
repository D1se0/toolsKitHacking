#!/bin/bash

# Función para actualizar el sistema e instalar tcpdump
instalar_tcpdump() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando tcpdump..."
    sudo apt-get install -y tcpdump

    if [ $? -eq 0 ]; then
        echo "[+] tcpdump se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar tcpdump."
    fi
}

# Ejecutar la función
instalar_tcpdump
