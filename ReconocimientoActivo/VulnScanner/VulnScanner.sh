#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner de inicio
echo -e "${BLUE}"
echo " ███▄ ▄███▓▓█████ ███▄    █  ▄████▄   ██ ▄█▀"
echo "▓██▒▀█▀ ██▒▓█   ▀ ██ ▀█   █ ▒██▀ ▀█   ██▄█▒ "
echo "▓██    ▓██░▒███  ▓██  ▀█ ██▒▒▓█    ▄ ▓███▄░ "
echo "▒██    ▒██ ▒▓█  ▄▓██▒  ▐▌██▒▒▓▓▄ ▄██▒▓██ █▄ "
echo "▒██▒   ░██▒░▒████▒██░   ▓██░▒ ▓███▀ ░▒██▒ █▄"
echo "░ ▒░   ░  ░░░ ▒░ ░ ▒░   ▒ ▒ ░ ░▒ ▒  ░▒ ▒▒ ▓▒"
echo "░  ░      ░ ░ ░  ░ ░░   ░ ▒░  ░  ▒   ░ ░▒ ▒░"
echo "░      ░      ░     ░   ░ ░ ░        ░ ░░ ░ "
echo "       ░      ░  ░        ░ ░ ░      ░  ░   "
echo "                           ░                "
echo -e "${NC}"

# Mostrar ayuda
function show_help() {
    echo -e "${YELLOW}Uso: ./VulnScanner.sh [opciones]${NC}"
    echo -e "Opciones:"
    echo -e "  -t, --target <dirección>     Especificar la dirección IP o URL para escanear"
    echo -e "  -p, --ports <puertos>         Especificar los puertos a escanear (ej. 80,443)"
    echo -e "  -x, --no-report               Omitir la generación de reportes .txt"
    echo -e "  -h, --help                    Mostrar esta ayuda"
}

# Variables predeterminadas
TARGET=""
PORTS="21,22,23,25,53,80,110,143,443,139,445,3389"
NO_REPORT=false

# Parsing de parámetros
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t|--target) TARGET="$2"; shift ;;
        -p|--ports) PORTS="$2"; shift ;;
        -x|--no-report) NO_REPORT=true ;;
        -h|--help) show_help; exit 0 ;;
        *) echo -e "${RED}Opción desconocida: $1${NC}"; show_help; exit 1 ;;
    esac
    shift
done

# Validar parámetros
if [[ -z "$TARGET" ]]; then
    echo -e "${RED}Debe especificar una dirección de destino con -t o --target.${NC}"
    show_help
    exit 1
fi

# Escaneo de puertos y servicios
echo -e "${GREEN}Iniciando escaneo de puertos en $TARGET...${NC}"
nmap -p $PORTS -sV $TARGET -oN nmap_results.txt
echo -e "${CYAN}Escaneo completado. Resultados guardados en nmap_results.txt${NC}"

# Buscar vulnerabilidades en Metasploit
echo -e "${GREEN}Buscando vulnerabilidades conocidas para los servicios detectados...${NC}"
while IFS= read -r line; do
    service=$(echo "$line" | awk '{print $3}')
    port=$(echo "$line" | awk -F'[ /]' '{print $5}')
    echo -e "${CYAN}Buscando exploits para el servicio $service en el puerto $port...${NC}"
    
    # Ejecutar Metasploit para buscar exploits
    msfconsole -q -x "search type:exploit platform:linux name:$service; exit" > msf_exploits.txt
    msfconsole -q -x "search type:exploit platform:windows name:$service; exit" >> msf_exploits.txt

    if [[ -s msf_exploits.txt ]]; then
        echo -e "${GREEN}Exploits encontrados para $service en el puerto $port:${NC}"
        cat msf_exploits.txt
    else
        echo -e "${RED}No se encontraron exploits para $service en el puerto $port.${NC}"
    fi
done < <(grep open nmap_results.txt)

# Preguntar al usuario si desea iniciar Metasploit
echo -e "${GREEN}¿Desea iniciar Metasploit para explotar las vulnerabilidades encontradas? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo -e "${CYAN}Iniciando Metasploit Framework...${NC}"
    msfconsole
fi

# Generar reporte si no se especifica -x
if [[ "$NO_REPORT" == false ]]; then
    echo -e "${GREEN}Generando reporte de escaneo y vulnerabilidades...${NC}"
    {
        echo "Resultados de Nmap:"
        cat nmap_results.txt
        echo
        echo "Exploits encontrados:"
        cat msf_exploits.txt
    } > report.txt
    echo -e "${CYAN}Reporte generado: report.txt${NC}"
else
    echo -e "${YELLOW}Omitiendo generación de reportes.${NC}"
fi

echo -e "${GREEN}\nEscaneo completo. Revise el archivo report.txt para más detalles si no se omitió.${NC}"
