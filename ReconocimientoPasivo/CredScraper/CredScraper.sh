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
    echo -e "  -k, --keyword <palabra_clave>  Especificar la palabra clave a buscar (por defecto: password|key|token)"
    echo -e "  -h, --help                     Mostrar esta ayuda"
}

# Variables
KEYWORD="password|key|token"

# Parsing de parámetros
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -k|--keyword) KEYWORD="$2"; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) echo -e "${RED}Opción desconocida: $1${NC}"; show_help; exit 1 ;;
    esac
    shift
done

# Verificar si la variable de entorno GITHUB_TOKEN está establecida
if [[ -z "$GITHUB_TOKEN" ]]; then
    echo -e "${RED}La variable de entorno GITHUB_TOKEN no está establecida.${NC}"
    echo -e "${YELLOW}Para configurar la variable, usa: export GITHUB_TOKEN='tu_token_aqui'${NC}"
    exit 1
fi

# Buscar en GitHub
echo -e "${GREEN}Buscando '${KEYWORD}' en todos los repositorios públicos de GitHub...${NC}"
RESULTS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/search/code?q=${KEYWORD}+in:file" | jq '.items[] | {name, path, html_url, repository: .repository.full_name}')

if [[ -z "$RESULTS" ]]; then
    echo -e "${RED}No se encontraron resultados en GitHub.${NC}"
else
    echo -e "${GREEN}Resultados de GitHub encontrados:${NC}"
    echo "$RESULTS" | jq -r '.'
fi

# Buscar en Google
echo -e "${GREEN}Buscando '${KEYWORD}' en Google...${NC}"
python3 -c "
from googlesearch import search
import sys

def google_search(query):
    results = search(query, num_results=10)
    for result in results:
        print(result)

google_search('${KEYWORD}')
"

# Escaneo de Google Cloud Storage
echo -e "${GREEN}Escaneando Google Cloud Storage...${NC}"
gcloud alpha storage ls --recursive | grep -E "${KEYWORD}" || echo -e "${RED}No se encontraron resultados en Google Cloud Storage.${NC}"

echo -e "${GREEN}\nBúsqueda completa. Revise los resultados anteriores.${NC}"
