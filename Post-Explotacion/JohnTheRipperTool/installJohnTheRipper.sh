#!/bin/bash

# Función para instalar John the Ripper
instalar_john_the_ripper() {
    echo "[+] Iniciando la instalación de John the Ripper..."

    # Actualizar lista de paquetes
    sudo apt update -y

    # Instalar dependencias necesarias
    echo "[+] Instalando dependencias..."
    sudo apt install -y build-essential libssl-dev zlib1g-dev

    # Instalar John the Ripper desde los repositorios oficiales
    echo "[+] Instalando John the Ripper..."
    sudo apt install -y john

    # Verificar instalación
    if command -v john &> /dev/null; then
        echo "[+] John the Ripper instalado correctamente."
        echo "[+] Versión instalada:"
        john --version
    else
        echo "[!] Error durante la instalación de John the Ripper."
    fi
}

# Función principal
main() {
    echo "[+] Verificando si John the Ripper ya está instalado..."
    if command -v john &> /dev/null; then
        echo "[+] John the Ripper ya está instalado."
        echo "[+] Versión instalada:"
        john --version
    else
        echo "[+] John the Ripper no está instalado. Procediendo a la instalación..."
        instalar_john_the_ripper
    fi
}

# Ejecutar función principal
main
