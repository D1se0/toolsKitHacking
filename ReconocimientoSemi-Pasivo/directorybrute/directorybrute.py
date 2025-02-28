#!/usr/bin/python3

import requests
import argparse
from colorama import Fore, Style
from tqdm import tqdm
import threading
import os
import queue

# Función para imprimir el logo en ASCII
def print_logo():
    logo = r"""
     ____  _                 _ _            _             
    |  _ \| | ___   ___ __ _| | | ___ _ __ | |_ _   _ ___ 
    | | | | |/ _ \ / __/ _` | | |/ _ \ '_ \| __| | | / __|
    | |_| | | (_) | (_| (_| | | |  __/ | | | |_| |_| \__ \
    |____/|_|\___/ \___\__,_|_|_|\___|_| |_|\__|\__,_|___/
    
                Directorybrute v1.0
                by Diseo (@d1se0)
    """
    return logo

# Variable global para indicar si se debe detener la ejecución de los hilos
stop_threads = False

# Función para limpiar la pantalla y actualizar la consola
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para realizar la solicitud HTTP
def check_url(queue, base_url, progress_bar, hidden_statuses, hidden_sizes, extensions, hidden_directories, collected_results):
    global stop_threads

    while not queue.empty() and not stop_threads:
        word = queue.get()
        try:
            response = requests.get(base_url.replace('BRUTE', word))
            content_length = len(response.content)
            status_code = response.status_code

            if status_code not in hidden_statuses and content_length not in hidden_sizes:
                result = f"{base_url.replace('BRUTE', word)} [{status_code}] - {content_length} bytes"
                print(f"\r{Fore.GREEN}[+]{Style.RESET_ALL} {result.ljust(os.get_terminal_size().columns - 1)}", end="")
                collected_results.append(result)
        except requests.exceptions.RequestException as e:
            print(f"\r{Fore.RED}[-]{Style.RESET_ALL} Error: {str(e).ljust(os.get_terminal_size().columns - 1)}", end="")
            stop_threads = True
            break

        progress_bar.update(1)

        for ext in extensions:
            if stop_threads:
                break

            try:
                response = requests.get(base_url.replace('BRUTE', f"{word}.{ext}"))
                content_length = len(response.content)
                status_code = response.status_code

                if status_code not in hidden_statuses and content_length not in hidden_sizes:
                    result = f"{base_url.replace('BRUTE', f'{word}.{ext}')} [{status_code}] - {content_length} bytes"
                    print(f"\r{Fore.GREEN}[+]{Style.RESET_ALL} {result.ljust(os.get_terminal_size().columns - 1)}", end="")
                    collected_results.append(result)
            except requests.exceptions.RequestException as e:
                print(f"\r{Fore.RED}[-]{Style.RESET_ALL} Error: {str(e).ljust(os.get_terminal_size().columns - 1)}", end="")
                stop_threads = True
                break

            progress_bar.update(1)
        
        queue.task_done()

# Función principal para manejar los argumentos y ejecutar los hilos
def main():
    global stop_threads

    logo = print_logo()
    print(Fore.CYAN + logo + Style.RESET_ALL)

    parser = argparse.ArgumentParser(
        description="Directorybrute: Herramienta para descubrir directorios ocultos y subdominios mediante fuerza bruta.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-w', '--wordlist', required=True, 
        help='Ruta al wordlist.'
    )
    parser.add_argument(
        '-t', '--threads', type=int, default=10, 
        help='Número de hilos para concurrencia (por defecto: 10).'
    )
    parser.add_argument(
        '-u', '--url', required=True, 
        help='URL con BRUTE donde se reemplazará para realizar la fuerza bruta (por ejemplo, "example.com/BRUTE").'
    )
    parser.add_argument(
        '--https', action='store_true', 
        help='Usar https en lugar de http.'
    )
    parser.add_argument(
        '--hp', '--hide-status', type=str, default='', 
        help='Ocultar códigos de estado HTTP específicos (por ejemplo, "200,202").'
    )
    parser.add_argument(
        '--hw', '--hide-size', type=str, default='', 
        help='Ocultar tamaños de contenido específicos (por ejemplo, "128,256").'
    )
    parser.add_argument(
        '-x', '--extensions', type=str, default='', 
        help='Extensiones a probar, separadas por comas (por ejemplo, "txt,html,php").'
    )
    parser.add_argument(
        '--hd', '--hidden-directories', action='store_true', 
        help='Añadir un punto delante de cada palabra para descubrir directorios o archivos ocultos.'
    )
    parser.add_argument(
        '-f', '--file', type=str, 
        help='Nombre del archivo para exportar los resultados.'
    )

    args = parser.parse_args()

    # Verificación de la palabra clave 'BRUTE' en la URL
    if 'BRUTE' not in args.url:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} La URL debe contener la palabra 'BRUTE' donde se reemplazará para realizar la fuerza bruta.")
        return

    # Verificación del protocolo HTTP/HTTPS
    if args.https and not args.url.startswith('https://'):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} No se ha especificado correctamente el protocolo 'https' en la URL.")
        return
    elif not args.https and args.url.startswith('https://'):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} No se ha especificado correctamente el protocolo 'http' en la URL.")
        return

    protocol = 'https' if args.https else 'http'
    base_url = args.url if args.url.startswith('http://') or args.url.startswith('https://') else f"{protocol}://{args.url}"

    hidden_statuses = {int(code) for code in args.hp.split(',') if code}
    hidden_sizes = {int(size) for size in args.hw.split(',') if size}
    extensions = [ext.strip() for ext in args.extensions.split(',') if ext]

    with open(args.wordlist, 'r', encoding='latin-1') as file:
        words = [line.strip() for line in file]

    if args.hd:
        words = ['.' + word for word in words]

    # Cola de tareas para distribuir entre los hilos
    task_queue = queue.Queue()
    for word in words:
        task_queue.put(word)

    total_words = len(words)

    # Configuración de la barra de progreso
    progress_bar = tqdm(total=total_words * (1 + len(extensions)), desc="Brute Forcing", unit="word", dynamic_ncols=True)

    # Lista para recopilar resultados
    collected_results = []

    # Crear y manejar hilos
    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=check_url, args=(task_queue, base_url, progress_bar, hidden_statuses, hidden_sizes, extensions, args.hd, collected_results))
        threads.append(t)
        t.start()

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[+]{Style.RESET_ALL} Saliendo...")
        stop_threads = True

    progress_bar.close()

    if args.file:
        with open(args.file, 'w') as f:
            f.write(logo + "\n\n")  # Escribir el logo al inicio del archivo

            # Escribir los resultados debajo del logo
            for result in collected_results:
                f.write(f"{result}\n")

if __name__ == "__main__":
    main()
