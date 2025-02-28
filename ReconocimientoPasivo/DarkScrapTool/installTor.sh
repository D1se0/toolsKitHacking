#!/bin/bash

# Función para instalar Tor
instalar_tor() {
    echo "[+] Iniciando la instalación de Tor..."

    # Actualizar lista de paquetes
    sudo apt update -y

    # Instalar Tor desde los repositorios oficiales
    echo "[+] Instalando Tor y sus dependencias..."
    sudo apt install -y tor tor-geoipdb

    # Verificar instalación
    if command -v tor &> /dev/null; then
        echo "[+] Tor instalado correctamente."
    else
        echo "[!] Error durante la instalación de Tor."
        exit 1
    fi
}

# Configurar Tor para que se inicie automáticamente con systemctl
configurar_autoinicio_tor() {
    echo "[+] Configurando Tor para que se inicie automáticamente al arrancar..."
    
    # Habilitar el servicio de Tor
    # sudo systemctl enable tor

    # Iniciar el servicio de Tor
    echo "[+] Iniciando el servicio de Tor..."
    sudo systemctl start tor

    # Verificar estado del servicio
    echo "[+] Verificando estado del servicio de Tor..."
    sudo systemctl status tor --no-pager
}

# Función principal
main() {
    echo "[+] Verificando si Tor ya está instalado..."
    if command -v tor &> /dev/null; then
        echo "[+] Tor ya está instalado."
        echo "[+] Estado actual del servicio de Tor:"
        sudo systemctl status tor --no-pager
    else
        echo "[+] Tor no está instalado. Procediendo a la instalación..."
        instalar_tor
        configurar_autoinicio_tor
    fi
}

# Ejecutar función principal
main
