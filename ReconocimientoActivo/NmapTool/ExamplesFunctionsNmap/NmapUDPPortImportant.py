#!/bin/python3

import re
from subprocess import run, PIPE

def validate_ip(ip):
    """Valida que una dirección IP sea válida."""
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if not ip_pattern.match(ip):
        return False
    # Verifica que cada octeto esté en el rango 0-255
    octets = ip.split('.')
    return all(0 <= int(octet) <= 255 for octet in octets)

def main():
    print("=" * 60)
    print("        ESCÁNER SNMP CON NMAP EN PUERTO 161          ")
    print("=" * 60)
    print("Este script realiza un escaneo de puertos UDP en el puerto 161\n"
          "en un host específico utilizando el escaneo UDP (-sU).\n")
    
    while True:
        ip = input("Por favor, introduce la dirección IP del host: ").strip()
        if validate_ip(ip):
            break
        else:
            print("❌ Dirección IP no válida. Asegúrate de que esté en el formato correcto (e.g., 192.168.1.1).\n")
    
    print(f"\nIniciando escaneo SNMP en el puerto 161 para el host: {ip}")
    print("=" * 60)

    # Ejecuta el comando nmap
    command = ["sudo", "nmap", "-v", "-sU", "-p161", ip]
    result = run(command, stdout=PIPE, stderr=PIPE, text=True)
    
    if result.returncode == 0:
        print("✅ Escaneo completado con éxito. Resultados:\n")
        print(result.stdout)
    else:
        print("❌ Ocurrió un error al ejecutar el escaneo.\n")
        print(result.stderr)
    
    print("=" * 60)
    print("                  FIN DEL ESCÁNER                     ")
    print("=" * 60)

if __name__ == "__main__":
    main()

