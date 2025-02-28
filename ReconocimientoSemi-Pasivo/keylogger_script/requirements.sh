#!/bin/bash

# Verificar si el script se está ejecutando como root
if [ "$(id -u)" -ne 0 ]; then
  echo "Este script debe ser ejecutado como root."
  exit 1
fi

# Actualizar el gestor de paquetes
echo "Actualizando el gestor de paquetes..."
apt-get update -y

# Instalar pip si no está instalado
echo "Instalando pip..."
apt-get install -y python3-pip

# Instalar paquetes de Python
echo "Instalando paquetes de Python..."
pip3 install pynput keyboard colorama

# Mensaje final
echo "Todos los paquetes han sido instalados."

# Verificación de la instalación
echo "Verificando las instalaciones..."
pip3 list
