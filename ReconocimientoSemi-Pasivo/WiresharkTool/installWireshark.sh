#!/bin/bash

# Función para actualizar el sistema e instalar Wireshark
instalar_wireshark() {
    echo "[+] Actualizando repositorios..."
    sudo apt update

    echo "[+] Instalando Wireshark..."
    sudo apt-get install -y wireshark

    if [ $? -eq 0 ]; then
        echo "[+] Wireshark se ha instalado correctamente."
    else
        echo "[!] Hubo un error al instalar Wireshark."
    fi
}

# Ejecutar la función
instalar_wireshark
