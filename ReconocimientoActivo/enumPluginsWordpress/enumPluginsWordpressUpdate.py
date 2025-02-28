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
    "contact-form-7",
    "yoast-seo",
    "elementor",
    "wordfence",
    "wp-super-cache",
    "wpforms",
    "all-in-one-seo-pack",
    "duplicate-post",
    "classic-editor",
    "updraftplus",
    "wordfence-security",
    "smush",
    "wp-mail-smtp",
    "nextgen-gallery",
    "redirection",
    "ithemes-security",
    "all-in-one-wp-migration",
    "tablepress",
    "mailpoet",
    "mailchimp-for-wp",
    "rank-math",
    "really-simple-ssl",
    "shortpixel-image-optimizer",
    "sucuri-scanner",
    "advanced-custom-fields",
    "disqus-comment-system",
    "simple-301-redirects",
    "wp-rocket",
    "autoptimize",
    "broken-link-checker",
    "easy-digital-downloads",
    "better-search-replace",
    "woocommerce-paypal-checkout-gateway",
    "popup-maker",
    "the-events-calendar",
    "seo-press",
    "backupbuddy",
    "slider-revolution",
    "visual-composer",
    "revslider",
    "wp-fastest-cache",
    "ninja-forms",
    "gravityforms",
    "dynamic-featured-image",
    "w3-total-cache",
    "loginizer",
    "monarch",
    "social-warfare",
    "ultimate-member",
    "advanced-ads",
    "pretty-links",
    "easy-social-share-buttons",
    "quiz-and-survey-master",
    "wp-job-manager",
    "bbpress",
    "buddypress",
    "memberpress",
    "lifterlms",
    "learndash",
    "caldera-forms",
    "hustle",
    "newsletter",
    "woocommerce-subscriptions",
    "woocommerce-memberships",
    "woocommerce-bookings"
]

def check_plugin(base_url, plugin):
    """
    Comprueba si el plugin existe en la URL base proporcionada y busca su versión.
    """
    url = f"{base_url}/wp-content/plugins/{plugin}/readme.txt"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Plugin encontrado: {plugin}")

            # Intentar extraer la versión del contenido del archivo
            version = get_version_from_readme(response.text)
            if version:
                print(f"    {Fore.CYAN}Versión detectada: {version}")
            else:
                print(f"    {Fore.YELLOW}[?] Versión no encontrada en el archivo.")
        else:
            pass  # Ignorar plugins no encontrados
    except requests.exceptions.RequestException:
        pass  # Silenciar errores de conexión

def get_version_from_readme(readme_content):
    """
    Intenta extraer la versión del plugin desde el contenido del archivo readme.txt.
    """
    for line in readme_content.splitlines():
        if "Version:" in line or "Stable tag:" in line:
            # Intentar capturar el valor después de "Version:" o "Stable tag:"
            return line.split(":")[1].strip()
    return None

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
    print(f"{Fore.CYAN}[*] Búsqueda completada. Sólo se muestran los plugins encontrados.")

if __name__ == "__main__":
    main()
