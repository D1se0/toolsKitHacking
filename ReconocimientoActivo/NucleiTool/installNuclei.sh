#!/bin/bash

# Función para instalar Nuclei
instalar_nuclei() {
    echo "[+] Iniciando la instalación de Nuclei..."

    # Actualizar lista de paquetes
    sudo apt update -y

    # Instalar dependencias necesarias
    echo "[+] Instalando dependencias..."
    sudo apt install -y wget unzip golang

    # Descargar la última versión de Nuclei
    echo "[+] Descargando Nuclei..."
    wget https://github.com/projectdiscovery/nuclei/releases/download/v2.9.3/nuclei_2.9.3_linux_amd64.zip

    # Descomprimir el archivo descargado
    echo "[+] Descomprimiendo Nuclei..."
    unzip nuclei_2.9.3_linux_amd64.zip

    # Mover el binario de Nuclei a /usr/local/bin
    echo "[+] Moviendo Nuclei a /usr/local/bin..."
    sudo mv nuclei /usr/local/bin/

    # Verificar instalación
    if command -v nuclei &> /dev/null; then
        echo "[+] Nuclei instalado correctamente."
    else
        echo "[!] Error durante la instalación de Nuclei."
        exit 1
    fi
}

# Función para configurar Nuclei (Opcional: Puedes añadir aquí configuraciones específicas)
configurar_nuclei() {
    echo "[+] Configurando Nuclei..."

    # Descargar plantillas de Nuclei (si no existen ya)
    if [ ! -d "$HOME/nuclei-templates" ]; then
        echo "[+] Descargando plantillas de Nuclei..."
        git clone https://github.com/projectdiscovery/nuclei-templates $HOME/nuclei-templates
    else
        echo "[+] Las plantillas de Nuclei ya están descargadas."
    fi
}

# Función principal
main() {
    echo "[+] Verificando si Nuclei ya está instalado..."
    if command -v nuclei &> /dev/null; then
        echo "[+] Nuclei ya está instalado."
    else
        echo "[+] Nuclei no está instalado. Procediendo a la instalación..."
        instalar_nuclei
        configurar_nuclei
    fi
}

# Ejecutar función principal
main
