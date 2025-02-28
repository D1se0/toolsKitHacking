#!/bin/bash

# Comprobar si se ejecuta como root
if [ "$(id -u)" -ne 0 ]; then
  echo "Este script debe ejecutarse como root. Usa 'sudo'."
  exit 1
fi

# Nombre del archivo .deb
DEB_FILE="Nessus-10.8.3-debian10_amd64.deb"

# Verificar si el archivo .deb existe
if [ ! -f "$DEB_FILE" ]; then
  echo "El archivo $DEB_FILE no se encuentra en el directorio actual."
  exit 1
fi

# Instalar Nessus
echo "Instalando Nessus..."
dpkg -i "$DEB_FILE"
if [ $? -ne 0 ]; then
  echo "Error durante la instalación. Intentando corregir dependencias..."
  apt-get install -f -y
  dpkg -i "$DEB_FILE"
  if [ $? -ne 0 ]; then
    echo "La instalación de Nessus falló."
    exit 1
  fi
fi

# Iniciar el servicio de Nessus
echo "Iniciando el servicio Nessus..."
systemctl start nessusd.service

# Habilitar el servicio para que inicie al arrancar el sistema
echo "Habilitando el servicio Nessus para el inicio automático..."
systemctl enable nessusd.service

# Esperar unos segundos para que el servicio se inicie completamente
echo "Esperando a que el servicio Nessus se inicie..."
sleep 10

# Abrir el navegador web en la URL de configuración
echo "Abriendo el navegador en https://localhost:8834/"
xdg-open "https://localhost:8834/"

echo "El proceso ha finalizado. Configura Nessus en tu navegador."
