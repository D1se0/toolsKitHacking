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
    print("      ESCÁNER DE PUERTOS CON NMAP PARA RANGO DE IPs      ")
    print("=" * 60)
    print("Este script realiza un escaneo avanzado de puertos en un\n"
          "rango de IPs y genera un archivo XML con los resultados.\n")
    
    while True:
        base_ip = input("Por favor, introduce la dirección IP base (e.g., 192.168.1.1): ").strip()
        if validate_ip(base_ip):
            break
        else:
            print("❌ Dirección IP base no válida. Asegúrate de que esté en el formato correcto.\n")
    
    while True:
        ip_range = input("Por favor, introduce el rango final de IPs (solo el último octeto, e.g., 100): ").strip()
        if ip_range.isdigit() and 0 <= int(ip_range) <= 255:
            break
        else:
            print("❌ Rango final no válido. Asegúrate de que sea un número entre 0 y 255.\n")
    
    full_range = f"{base_ip}-{ip_range}"
    print(f"\nIniciando escaneo para el rango: {full_range}")
    print("=" * 60)

    # Ejecuta el comando nmap
    command = [
        "sudo", "nmap", "-v", "--reason", "-sS",
        "-oX", "puertos.xml",
        '--stylesheet=https://svn.nmap.org/nmap/docs/nmap.xsl',
        full_range
    ]
    result = run(command, stdout=PIPE, stderr=PIPE, text=True)
    
    if result.returncode == 0:
        print("✅ Escaneo completado con éxito. Los resultados se han guardado en 'puertos.xml'.\n")
        print(result.stdout)
    else:
        print("❌ Ocurrió un error al ejecutar el escaneo.\n")
        print(result.stderr)
    
    print("=" * 60)
    print("                  FIN DEL ESCÁNER                     ")
    print("=" * 60)

if __name__ == "__main__":
    main()

