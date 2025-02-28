#!/bin/bash

# Función para actualizar el sistema e instalar Burp Suite
instalar_burp_suite() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando Burp Suite..."
    sudo apt install -y burpsuite

    if [ $? -eq 0 ]; then
        echo "[+] Burp Suite se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar Burp Suite."
    fi
}

# Ejecutar la función
instalar_burp_suite
