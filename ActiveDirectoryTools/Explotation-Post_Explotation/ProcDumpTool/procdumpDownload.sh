#!/bin/bash

# Enlace que se abrirá
LINK="https://learn.microsoft.com/es-es/sysinternals/downloads/procdump"

# Función para instalar paquetes necesarios
instalar_dependencias() {
    echo "[+] Verificando dependencias..."
    
    # Verificar si xdg-open está disponible
    if ! command -v xdg-open &> /dev/null; then
        echo "[!] xdg-open no está instalado. Instalándolo..."
        sudo apt update && sudo apt install -y xdg-utils
    else
        echo "[+] xdg-open ya está instalado."
    fi

    # Verificar si Firefox está disponible (u otro navegador)
    if ! command -v firefox &> /dev/null; then
        echo "[!] Firefox no está instalado. Instalándolo..."
        sudo apt update && sudo apt install -y firefox-esr
    else
        echo "[+] Firefox ya está instalado."
    fi
}

# Función para cerrar Firefox si está abierto
cerrar_firefox() {
    if pgrep -x "firefox" > /dev/null; then
        echo "[+] Firefox está abierto. Cerrándolo..."
        pkill -x firefox
        sleep 2  # Esperar unos segundos para asegurarse de que se cierre
    else
        echo "[+] Firefox no está abierto."
    fi
}

# Función para abrir el enlace
abrir_enlace() {
    echo "[+] Abriendo el enlace en el navegador..."
    xdg-open "$LINK"
}

# Ejecutar funciones
instalar_dependencias
cerrar_firefox
abrir_enlace
