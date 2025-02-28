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

def validate_ports(ports):
    """Valida que los puertos sean una lista de números separados por comas."""
    port_pattern = re.compile(r'^(\d{1,5})(,\d{1,5})*$')
    if not port_pattern.match(ports):
        return False
    # Verifica que cada puerto esté en el rango 1-65535
    return all(1 <= int(port) <= 65535 for port in ports.split(','))

def main():
    print("=" * 60)
    print("       ESCÁNER DE PUERTOS ESPECÍFICOS CON NMAP          ")
    print("=" * 60)
    print("Este script realiza un escaneo de servicios y versiones\n"
          "en puertos específicos de un host dado.\n")
    
    while True:
        ip = input("Por favor, introduce la dirección IP del host: ").strip()
        if validate_ip(ip):
            break
        else:
            print("❌ Dirección IP no válida. Asegúrate de que esté en el formato correcto (e.g., 192.168.1.1).\n")
    
    while True:
        ports = input("Por favor, introduce los puertos a escanear separados por comas (e.g., 22,80,443): ").strip()
        if validate_ports(ports):
            break
        else:
            print("❌ Lista de puertos no válida. Asegúrate de que sean números separados por comas, entre 1 y 65535.\n")
    
    print(f"\nIniciando escaneo para el host: {ip} en los puertos: {ports}")
    print("=" * 60)

    # Ejecuta el comando nmap
    command = ["nmap", "-sCV", f"-p{ports}", ip]
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

