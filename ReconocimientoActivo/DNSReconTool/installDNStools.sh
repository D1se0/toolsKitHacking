#!/bin/bash

# Función para actualizar el sistema e instalar dnstools
instalar_dnstools() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando dnstools..."
    sudo apt-get install -y dnsutils

    if [ $? -eq 0 ]; then
        echo "[+] dnstools (dnsutils) se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar dnstools."
    fi
}

# Ejecutar la función
instalar_dnstools
