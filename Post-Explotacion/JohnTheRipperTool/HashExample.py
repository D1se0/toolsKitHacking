#!/bin/python3

import hashlib
import os

# Colores para la terminal
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Función para mostrar el banner inicial
def print_banner():
    """Muestra el banner de inicio."""
    print(f"""
{CYAN}{BOLD}--------------------------------------------
|      HASHEADOR DE CONTRASEÑAS EN PYTHON    |
--------------------------------------------{RESET}
""")

# Función para mostrar el menú de opciones de hash
def print_hash_options():
    """Muestra las opciones de hash al usuario."""
    print(f"{CYAN}{BOLD}Selecciona el tipo de hash para generar:{RESET}")
    print(f"{YELLOW}1. MD5{RESET}")
    print(f"{YELLOW}2. SHA1{RESET}")
    print(f"{YELLOW}3. SHA256{RESET}")
    print(f"{YELLOW}4. SHA512{RESET}")

# Función para pedir una palabra al usuario y asegurarse de que no esté vacía
def get_word_input():
    """Solicita la palabra a hashear al usuario."""
    while True:
        word = input(f"{YELLOW}Introduce la palabra a hashear:{RESET} ")
        if word.strip():
            return word
        else:
            print(f"{RED}La palabra no puede estar vacía. Inténtalo de nuevo.{RESET}")

# Función para pedir la opción de hash al usuario y validarla
def get_hash_option():
    """Solicita al usuario seleccionar el tipo de hash."""
    while True:
        try:
            choice = int(input(f"{YELLOW}Selecciona el número de opción (1-4):{RESET} "))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print(f"{RED}Opción no válida. Elige entre 1 y 4.{RESET}")
        except ValueError:
            print(f"{RED}Por favor, ingresa un número válido.{RESET}")

# Función para generar el hash según el tipo elegido
def generate_hash(word, option):
    """Genera el hash de la palabra según la opción seleccionada."""
    if option == 1:
        return hashlib.md5(word.encode()).hexdigest()
    elif option == 2:
        return hashlib.sha1(word.encode()).hexdigest()
    elif option == 3:
        return hashlib.sha256(word.encode()).hexdigest()
    elif option == 4:
        return hashlib.sha512(word.encode()).hexdigest()

# Función para guardar el hash en un archivo
def save_hash_to_file(hash_value, hash_type):
    """Guarda el hash generado en un archivo con el tipo de hash como nombre."""
    file_name = f"hash.{hash_type}"
    with open(file_name, "w") as file:
        file.write(hash_value)
    print(f"{GREEN}El hash se ha guardado exitosamente en el archivo {file_name}{RESET}")

# Función principal del script
def main():
    """Función principal que ejecuta todo el flujo."""
    print_banner()

    # Solicitar palabra a hashear
    word = get_word_input()

    # Mostrar opciones de tipo de hash y obtener selección del usuario
    print_hash_options()
    option = get_hash_option()

    # Generar el hash
    hash_value = generate_hash(word, option)

    # Seleccionar el tipo de hash
    hash_types = {1: "md5", 2: "sha1", 3: "sha256", 4: "sha512"}
    hash_type = hash_types[option]

    # Guardar el hash en un archivo
    save_hash_to_file(hash_value, hash_type)

if __name__ == "__main__":
    main()
