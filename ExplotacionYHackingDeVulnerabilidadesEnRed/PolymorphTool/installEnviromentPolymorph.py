#!/bin/python3

import os
import subprocess
import sys

# Colores para la terminal
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

def print_banner():
    """Print a banner to introduce the script."""
    print(f"""
{CYAN}{BOLD}--------------------------------------------
|       POLYMORPH ENVIRONMENT SETUP         |
--------------------------------------------{RESET}
""")

def check_root():
    """Check if the script is running as root."""
    if os.geteuid() != 0:
        print(f"{RED}{BOLD}[ERROR] Este script debe ejecutarse como root.{RESET}")
        print(f"{YELLOW}Usa 'sudo' para ejecutarlo correctamente.{RESET}")
        sys.exit(1)
    else:
        print(f"{GREEN}{BOLD}[OK] Permisos de root verificados.{RESET}")

def create_virtualenv():
    """Create a virtual environment."""
    env_name = "PolymorphEnviroment"
    print(f"\n{CYAN}{BOLD}[INFO] Creando el entorno virtual '{env_name}'...{RESET}")
    subprocess.run(["python3", "-m", "venv", env_name], check=True)
    activate_script = f"./{env_name}/bin/activate"
    print(f"{GREEN}{BOLD}[OK] Entorno virtual '{env_name}' creado exitosamente.{RESET}")
    print(f"{YELLOW}Usa este comando para activar el entorno virtual manualmente:\nsource {activate_script}{RESET}")
    return activate_script

def run_commands():
    """Run the required commands."""
    commands = [
        "sudo apt update",
        "sudo apt install -y build-essential python3-dev libnetfilter-queue-dev tshark tcpdump python3-pip wireshark git",
        "pip3 install git+https://github.com/kti/python-netfilterqueue",
        "pip3 install polymorph"
    ]

    for command in commands:
        print(f"\n{CYAN}{BOLD}[INFO] Ejecutando: {command}{RESET}")
        subprocess.run(command, shell=True, check=True)
        print(f"{GREEN}{BOLD}[OK] Comando completado: {command.split()[0]}{RESET}")

def run_polymorph():
    """Launch the Polymorph tool."""
    print(f"\n{CYAN}{BOLD}[INFO] Iniciando la herramienta 'polymorph'...{RESET}")
    subprocess.run(["polymorph"], check=True)

if __name__ == "__main__":
    print_banner()
    check_root()
    activate_script = create_virtualenv()
    run_commands()
    print(f"\n{YELLOW}Ahora puedes activar el entorno virtual usando:{RESET}")
    print(f"{CYAN}{BOLD}source {activate_script}{RESET}")
    print(f"{CYAN}{BOLD}[INFO] Todo está listo. Ejecutando Polymorph...{RESET}")
    run_polymorph()
