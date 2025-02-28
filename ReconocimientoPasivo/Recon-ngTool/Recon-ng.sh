#!/bin/bash

# Función para verificar si Recon-ng está instalado
check_reconng() {
    if command -v recon-ng &> /dev/null; then
        return 0  # Recon-ng está instalado
    else
        return 1  # Recon-ng no está instalado
    fi
}

# Instalar Recon-ng si no está instalado
install_reconng() {
    echo "[+] Recon-ng no encontrado. Instalando..."
    sudo apt update
    sudo apt install -y recon-ng
}

# Ejecutar Recon-ng
run_reconng() {
    echo "[+] Ejecutando Recon-ng..."
    recon-ng
}

# Verificar si Recon-ng está instalado
check_reconng
if [ $? -eq 0 ]; then
    echo "[+] Recon-ng ya está instalado."
    run_reconng
else
    install_reconng
    run_reconng
fi
