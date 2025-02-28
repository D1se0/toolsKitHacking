import requests
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

# Lista de plugins
plugins = [
    "jetpack",
    "site-editor",
    "akismet",
    "woocommerce",
    "elementor",
    "contact-form-7",
]

def check_plugin(base_url, plugin):
    """
    Comprueba si el plugin existe en la URL base proporcionada.
    """
    url = f"{base_url}/wp-content/plugins/{plugin}/readme.txt"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Plugin encontrado: {plugin}")
        else:
            print(f"{Fore.YELLOW}[-] Plugin no encontrado: {plugin}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error al conectar con {url}: {e}")

def main():
    """
    Función principal del script.
    """
    print(f"{Fore.CYAN}[*] Bienvenido al buscador de plugins de WordPress")
    print(f"{Fore.CYAN}[*] Por favor, introduce la URL del sitio de WordPress a analizar.")
    
    # Solicitar la URL al usuario
    base_url = input(f"{Fore.BLUE}Introduce la URL (ejemplo: http://example.com): ").strip()

    # Verificar si la URL incluye el protocolo
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        base_url = f"http://{base_url}"

    print(f"{Fore.CYAN}[*] Comenzando la búsqueda de plugins en: {base_url}")
    print(f"{Fore.CYAN}[*] Plugins a buscar: {', '.join(plugins)}")
    print("-" * 50)

    # Comprobar cada plugin
    for plugin in plugins:
        check_plugin(base_url, plugin)

    print("-" * 50)
    print(f"{Fore.CYAN}[*] Búsqueda completada.")

if __name__ == "__main__":
    main()
