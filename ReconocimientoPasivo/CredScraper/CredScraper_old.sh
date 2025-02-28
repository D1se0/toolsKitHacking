#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Banner de inicio
echo -e "${YELLOW}"
echo " ██████╗██████╗ ███████╗██████╗     ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ "
echo "██╔════╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗"
echo "██║     ██████╔╝█████╗  ██████╔╝    ███████╗██║     ██████╔╝███████║██║  ██║█████╗  ██████╔╝"
echo "██║     ██╔═══╝ ██╔══╝  ██╔══██╗    ╚════██║██║     ██╔══██╗██╔══██║██║  ██║██╔══╝  ██╔══██╗"
echo "╚██████╗██║     ███████╗██║  ██║    ███████║╚██████╗██║  ██║██║  ██║██████╔╝███████╗██║  ██║"
echo " ╚═════╝╚═╝     ╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝"
echo -e "${NC}"

# Mostrar ayuda
function show_help() {
    echo -e "${YELLOW}Uso: ./credscraper.sh [opciones]${NC}"
    echo -e "Opciones:"
    echo -e "  -u, --user <usuario>           Especificar el usuario de GitHub"
    echo -e "  -r, --repo <repositorio>       Especificar el repositorio a escanear"
    echo -e "  -k, --keyword <palabra_clave>  Especificar la palabra clave a buscar (por defecto: password|key|token)"
    echo -e "  -h, --help                     Mostrar esta ayuda"
}

# Variables
USER=""
REPO=""
KEYWORD="password|key|token"

# Parsing de parámetros
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -u|--user) USER="$2"; shift ;;
        -r|--repo) REPO="$2"; shift ;;
        -k|--keyword) KEYWORD="$2"; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) echo -e "${RED}Opción desconocida: $1${NC}"; show_help; exit 1 ;;
    esac
    shift
done

# Comprobaciones iniciales
if [[ -z "$USER" || -z "$REPO" ]]; then
    echo -e "${RED}Debe especificar tanto el usuario como el repositorio.${NC}"
    show_help
    exit 1
fi

# Verificar si la variable de entorno GITHUB_TOKEN está establecida
if [[ -z "$GITHUB_TOKEN" ]]; then
    echo -e "${RED}La variable de entorno GITHUB_TOKEN no está establecida.${NC}"
    echo -e "${YELLOW}Para configurar la variable, usa: export GITHUB_TOKEN='tu_token_aqui'${NC}"
    exit 1
fi

# Búsqueda de palabras clave en GitHub usando la API
echo -e "${GREEN}Buscando '${KEYWORD}' en el repositorio ${USER}/${REPO}...${NC}"
RESULTS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/search/code?q=${KEYWORD}+in:file+repo:${USER}/${REPO}" | jq '.items[] | {name, path, html_url}')

if [[ -z "$RESULTS" ]]; then
    echo -e "${RED}No se encontraron resultados para la búsqueda.${NC}"
else
    echo -e "${GREEN}Resultados encontrados:${NC}"
    echo "$RESULTS" | jq -r '.'
fi

echo -e "${GREEN}\nBúsqueda completa. Revise los resultados anteriores.${NC}"
