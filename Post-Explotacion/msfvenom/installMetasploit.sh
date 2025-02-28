#!/bin/bash

# Función para instalar Metasploit Framework
instalar_metasploit() {
    echo "[+] Iniciando la instalación de Metasploit Framework..."

    # Actualizar lista de paquetes
    sudo apt update -y

    # Instalar dependencias requeridas
    echo "[+] Instalando dependencias..."
    sudo apt install -y curl gnupg2

    # Descargar e instalar el script oficial de instalación
    echo "[+] Descargando e instalando Metasploit..."
    curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb -o msfinstall
    chmod +x msfinstall
    sudo ./msfinstall

    # Verificar instalación
    if command -v msfconsole &> /dev/null; then
        echo "[+] Metasploit Framework instalado correctamente."
        echo "[+] Versión instalada:"
        msfconsole --version
    else
        echo "[!] Error durante la instalación de Metasploit Framework."
    fi

    # Limpiar el archivo de instalación
    rm -f msfinstall
}

# Función principal
main() {
    echo "[+] Verificando si Metasploit ya está instalado..."
    if command -v msfconsole &> /dev/null; then
        echo "[+] Metasploit Framework ya está instalado."
        echo "[+] Versión instalada:"
        msfconsole --version
    else
        echo "[+] Metasploit no está instalado. Procediendo a la instalación..."
        instalar_metasploit
    fi
}

# Ejecutar función principal
main
