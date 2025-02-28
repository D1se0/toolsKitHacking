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
    print("    ESCÁNER DE VULNERABILIDADES CON NMAP PARA DOS IPs     ")
    print("=" * 60)
    print("Este script realiza un escaneo de vulnerabilidades en dos direcciones\n"
          "IP proporcionadas, utilizando el script de Nmap para buscar vulnerabilidades\n"
          "en los servicios de ambas IPs especificadas.\n")
    
    # Validación de la primera IP (completa)
    while True:
        ip1 = input("Por favor, introduce la dirección IP completa (ej. 10.10.11.22) para la primera IP del host: ").strip()
        if validate_ip(ip1):
            break
        else:
            print("❌ Dirección IP no válida. Asegúrate de que esté en el formato correcto (e.g., 10.10.11.22).\n")
    
    # Validación de la segunda IP (número final)
    while True:
        try:
            ip2_last = int(input(f"Por favor, introduce el número final de la segunda IP (ej. 25 para 10.10.11.25): ").strip())
            if 0 <= ip2_last <= 255:
                ip2 = f"{ip1.rsplit('.', 1)[0]}.{ip2_last}"  # Construye la segunda IP con el número final
                break
            else:
                print("❌ El número final debe estar entre 0 y 255.\n")
        except ValueError:
            print("❌ Por favor, ingresa un número válido para la última parte de la IP.\n")

    print(f"\nIniciando escaneo de vulnerabilidades para las IPs: {ip1} y {ip2}")
    print("=" * 60)

    # Ejecuta el comando nmap con el formato correcto
    command = [
        "sudo", "nmap", "-v", "-sS", "-oX", "vulnerabilidadesTCP.xml",
        f'--stylesheet="https://svn.nmap.org/nmap/docs/nmap.xsl"',
        "--script=vuln", f"{ip1},{ip2}"
    ]
    
    # Ejecutar el comando y obtener el resultado
    result = run(" ".join(command), shell=True, stdout=PIPE, stderr=PIPE, text=True)
    
    if result.returncode == 0:
        print("✅ Escaneo completado con éxito. Resultados guardados en vulnerabilidadesTCP.xml.\n")
        print(result.stdout)
    else:
        print("❌ Ocurrió un error al ejecutar el escaneo.\n")
        print(result.stderr)
    
    print("=" * 60)
    print("                  FIN DEL ESCÁNER                     ")
    print("=" * 60)

if __name__ == "__main__":
    main()
