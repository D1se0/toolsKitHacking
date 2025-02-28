#!/bin/python3

import os
import subprocess
import sys

# Función para ejecutar comandos en la terminal
def run_command(command):
    """Ejecuta un comando en la terminal y maneja posibles errores."""
    try:
        print(f"Ejecutando: {command}")
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        sys.exit(1)

def install_batea():
    """Instala BATEA en un entorno virtual de Anaconda/Miniconda."""
    
    # Paso 1: Crear un nuevo entorno en conda
    print("Paso 1: Creando un nuevo entorno virtual en Anaconda/Miniconda (batea_env)...")
    run_command("conda create -n batea_env pip python=3.7 -y")
    
    # Paso 2: Activar el entorno virtual
    print("Paso 2: Activando el entorno virtual 'batea_env'...")
    run_command("conda activate batea_env")
    
    # Paso 3: Acceder a la carpeta donde se encuentra BATEA
    print("Paso 3: Accediendo a la carpeta 'batea'...")

    # Cambia esta ruta a la carpeta donde tienes BATEA descargado
    batea_directory = "batea/"  # Modifica esta ruta
    os.chdir(batea_directory)

    # Paso 4: Instalar los requisitos
    print("Paso 4: Instalando los paquetes requeridos desde 'requirements.txt'...")
    run_command("pip install -r requirements.txt")
    
    # Paso 5: Instalar BATEA
    print("Paso 5: Instalando BATEA...")
    run_command("pip install -e .")
    
    # Paso 6: Ejecutar BATEA
    print("Paso 6: Ejecutando BATEA...")
    run_command("batea")
    run_command("batea")

# Ejecutar el script de instalación
if __name__ == "__main__":
    install_batea()
