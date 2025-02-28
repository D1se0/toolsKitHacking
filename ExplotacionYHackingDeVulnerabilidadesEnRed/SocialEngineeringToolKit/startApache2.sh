#!/bin/bash

echo "[+] Iniciando apache2..."
systemctl start apache2
systemctl enable apache2
echo "[+] apache2 iniciado y vinculado con arranque"
