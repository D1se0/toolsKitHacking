#!/bin/bash

# Función para instalar srm
instalar_srm() {
    echo "[+] Iniciando la instalación de srm..."

    # Actualizar lista de paquetes
    sudo apt update -y

    # Instalar srm desde los repositorios oficiales
    echo "[+] Instalando srm..."
    sudo apt install -y secure-delete

    # Verificar instalación
    if command -v srm &> /dev/null; then
        echo "[+] srm instalado correctamente."
        echo "[+] Versión instalada:"
        srm --version
    else
        echo "[!] Error durante la instalación de srm."
    fi
}

# Función principal
main() {
    echo "[+] Verificando si srm ya está instalado..."
    if command -v srm &> /dev/null; then
        echo "[+] srm ya está instalado."
        echo "[+] Versión instalada:"
        srm --version
    else
        echo "[+] srm no está instalado. Procediendo a la instalación..."
        instalar_srm
    fi
}

# Ejecutar función principal
main
