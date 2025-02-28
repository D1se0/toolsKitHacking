#!/bin/python3

import os
import re
from subprocess import run, PIPE

def validate_ip(ip):
    """Valida que la IP sea válida y termine en .0."""
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}0$')
    if not ip_pattern.match(ip):
        return False
    # Verifica que cada octeto esté en el rango 0-255
    octets = ip.split('.')
    return all(0 <= int(octet) <= 255 for octet in octets[:-1])

def main():
    print("=" * 50)
    print("           ESCÁNER DE RED LOCAL (NMAP)           ")
    print("=" * 50)
    print("Este script escaneará dispositivos en tu segmento de red.\n")
    
    while True:
        ip = input("Por favor, introduce la dirección IP base (terminada en .0): ").strip()
        if validate_ip(ip):
            break
        else:
            print("❌ Dirección IP no válida. Asegúrate de que termine en '.0' y esté en el formato correcto.\n")
    
    print("\nIniciando escaneo con Nmap...")
    print("=" * 50)

    # Ejecuta el comando nmap
    command = ["nmap", "-sn", f"{ip}/24"]
    result = run(command, stdout=PIPE, stderr=PIPE, text=True)
    
    if result.returncode == 0:
        print("✅ Escaneo completado con éxito. Resultados:\n")
        print(result.stdout)
    else:
        print("❌ Ocurrió un error al ejecutar el escaneo.\n")
        print(result.stderr)
    
    print("=" * 50)
    print("               FIN DEL ESCÁNER                   ")
    print("=" * 50)

if __name__ == "__main__":
    main()

