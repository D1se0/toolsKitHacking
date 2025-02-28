#!/usr/bin/env python3

import re
import sys
import subprocess

def extract_ports(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print("File not found!")
        return

    # Extraer la dirección IP
    ip_match = re.search(r'^Host: ([\d\.]+)', content, re.MULTILINE)
    ip_address = ip_match.group(1) if ip_match else None

    if ip_address:
        print(f"\t[*] IP Address: {ip_address}")
    else:
        print("No IP address found or extraction failed.")
        return

    # Extraer los puertos abiertos
    ports = re.findall(r'(\d{1,5})/open', content)
    if ports:
        ports_str = ','.join(ports)
        print(f"\t[*] Open ports: {ports_str}")
    else:
        print("No ports found or extraction failed.")
        return

    # Verificar si xclip está instalado
    try:
        subprocess.run(['xclip', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("[*] xclip is not installed. Ports not copied to clipboard.")
        return

    # Copiar los puertos al portapapeles si xclip está disponible
    try:
        subprocess.run(['xclip', '-sel', 'clip'], input=ports_str.encode(), check=True)
        print("[*] Ports copied to clipboard")
    except subprocess.CalledProcessError as e:
        print(f"[*] Failed to copy ports to clipboard: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)
    
    extract_ports(sys.argv[1])
