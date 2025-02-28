#!/bin/bash

# Función para instalar Shred
instalar_shred() {
    echo "[+] Iniciando la instalación de Shred..."

    # Actualizar lista de paquetes
    sudo apt update -y

    # Instalar Shred desde los repositorios oficiales
    echo "[+] Instalando Shred..."
    sudo apt install -y coreutils

    # Verificar instalación
    if command -v shred &> /dev/null; then
        echo "[+] Shred instalado correctamente."
        echo "[+] Versión instalada:"
        shred --version
    else
        echo "[!] Error durante la instalación de Shred."
    fi
}

# Función principal
main() {
    echo "[+] Verificando si Shred ya está instalado..."
    if command -v shred &> /dev/null; then
        echo "[+] Shred ya está instalado."
        echo "[+] Versión instalada:"
        shred --version
    else
        echo "[+] Shred no está instalado. Procediendo a la instalación..."
        instalar_shred
    fi
}

# Ejecutar función principal
main
