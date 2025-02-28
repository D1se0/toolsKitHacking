#!/bin/python3

import os
import subprocess
import sys
import shutil

def install_package(package_name):
    """Instala un paquete usando apt-get o pip3."""
    try:
        print(f"\033[1;34mInstalando {package_name}...\033[0m")
        subprocess.check_call(["sudo", "apt-get", "install", "-y", package_name])
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mError al instalar {package_name}: {e}\033[0m")
        sys.exit(1)

def check_python_venv():
    """Verifica si python3-venv está instalado, y si no lo instala."""
    try:
        subprocess.check_call(["python3", "-m", "venv", "testenv"])
        # Si el entorno virtual de prueba se creó, eliminamos la carpeta de forma segura
        shutil.rmtree("testenv", ignore_errors=True)
    except subprocess.CalledProcessError:
        print("\033[1;31mpython3-venv no está instalado. Instalando...\033[0m")
        install_package("python3-venv")

def install_requirements():
    """Instala las dependencias de requirements.txt."""
    try:
        # Cambiar al directorio XSStrike
        print("\033[1;32mCambiando al directorio XSStrike...\033[0m")
        os.chdir("XSStrike")

        # Intentar instalar las dependencias globalmente
        print("\033[1;32mIntentando instalar dependencias globalmente...\033[0m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mError al instalar dependencias globalmente: {e}\033[0m")
        print("\033[1;33mIntentando crear un entorno virtual de Python...\033[0m")
        
        # Crear entorno virtual
        subprocess.check_call([sys.executable, "-m", "venv", "xsstrikeEnviroment"])
        print("\033[1;32mEntorno virtual creado.\033[0m")

        # Activar el entorno virtual utilizando subprocess.run()
        activate_script = "./xsstrikeEnviroment/bin/activate"
        print("\033[1;32mActivando el entorno virtual...\033[0m")
        subprocess.run([f"source {activate_script} && pip3 install -r requirements.txt"], shell=True, executable="/bin/bash")

def run_xsstrike():
    """Ejecuta XSStrike con el parámetro -h para verificar que todo funciona."""
    print("\033[1;32mEjecutando XSStrike...\033[0m")
    subprocess.check_call(["python3", "xsstrike.py", "-h"])

def main():
    """Función principal que coordina la instalación y ejecución."""
    print("\033[1;36mBienvenido al instalador automático de XSStrike!\033[0m")
    
    # Asegúrate de que python3-pip esté instalado
    install_package("python3-pip")

    # Verificar que python3-venv esté disponible y, si no, instalarlo
    check_python_venv()

    # Instalar las dependencias y ejecutar XSStrike
    install_requirements()
    run_xsstrike()

    print("\033[1;32m¡Instalación y configuración completadas con éxito!\033[0m")

if __name__ == "__main__":
    main()
