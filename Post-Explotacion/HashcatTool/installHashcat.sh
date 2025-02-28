#!/bin/bash

# Función para instalar Hashcat
instalar_hashcat() {
    echo "[+] Iniciando la instalación de Hashcat..."

    # Actualizar lista de paquetes
    sudo apt update -y

    # Instalar dependencias necesarias
    echo "[+] Instalando dependencias..."
    sudo apt install -y build-essential checkinstall libssl-dev zlib1g-dev libcuda1-455

    # Instalar Hashcat desde los repositorios oficiales
    echo "[+] Instalando Hashcat..."
    sudo apt install -y hashcat

    # Verificar instalación
    if command -v hashcat &> /dev/null; then
        echo "[+] Hashcat instalado correctamente."
        echo "[+] Versión instalada:"
        hashcat --version
    else
        echo "[!] Error durante la instalación de Hashcat."
    fi
}

# Función principal
main() {
    echo "[+] Verificando si Hashcat ya está instalado..."
    if command -v hashcat &> /dev/null; then
        echo "[+] Hashcat ya está instalado."
        echo "[+] Versión instalada:"
        hashcat --version
    else
        echo "[+] Hashcat no está instalado. Procediendo a la instalación..."
        instalar_hashcat
    fi
}

# Ejecutar función principal
main
