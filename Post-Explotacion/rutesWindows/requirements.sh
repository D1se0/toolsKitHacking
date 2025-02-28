#!/bin/bash

# Nombre del script
SCRIPT_NAME="requirements.sh"

echo ">>> $SCRIPT_NAME: Starting installation process."

# Función para verificar si un comando está instalado
command_exists() {
    command -v "$1" &> /dev/null
}

# Detectar gestor de paquetes
if command_exists apt; then
    PACKAGE_MANAGER="apt"
    UPDATE_CMD="sudo apt update"
    INSTALL_CMD="sudo apt install -y"
elif command_exists yum; then
    PACKAGE_MANAGER="yum"
    UPDATE_CMD="sudo yum update -y"
    INSTALL_CMD="sudo yum install -y"
else
    echo ">>> $SCRIPT_NAME: Error - Supported package manager not found (apt or yum)."
    exit 1
fi

echo ">>> $SCRIPT_NAME: Detected package manager: $PACKAGE_MANAGER"

# Actualizar lista de paquetes
echo ">>> $SCRIPT_NAME: Updating package lists..."
$UPDATE_CMD

# Instalar dependencias del sistema
echo ">>> $SCRIPT_NAME: Installing system dependencies..."
$INSTALL_CMD python3 python3-pip python3-venv

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo ">>> $SCRIPT_NAME: Creating Python virtual environment..."
    python3 -m venv venv
else
    echo ">>> $SCRIPT_NAME: Virtual environment already exists. Skipping creation."
fi

# Activar entorno virtual
echo ">>> $SCRIPT_NAME: Activating virtual environment..."
source venv/bin/activate

# Crear archivo requirements.txt
echo ">>> $SCRIPT_NAME: Creating requirements.txt..."
cat << EOF > requirements.txt
argparse
colorama
readline
EOF

# Instalar dependencias de Python
echo ">>> $SCRIPT_NAME: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ">>> $SCRIPT_NAME: All dependencies installed successfully."

# Recordatorio
echo ">>> $SCRIPT_NAME: To run the script, activate the virtual environment using:"
echo "    source venv/bin/activate"
