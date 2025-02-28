#!/bin/bash

# Colores para hacer el script atractivo
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # Sin color

# Banner inicial
echo -e "${BLUE}"
echo "##############################################"
echo "#                                            #"
echo "#        Instalador de CUPP (v1.0)           #"
echo "#                                            #"
echo "##############################################"
echo -e "${NC}"

# Comprobación de permisos de administrador
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Este script debe ejecutarse como root.${NC}"
  exit 1
fi

# Actualizar repositorios
echo -e "${YELLOW}Actualizando los repositorios del sistema...${NC}"
if apt-get update; then
  echo -e "${GREEN}[OK] Repositorios actualizados.${NC}"
else
  echo -e "${RED}[ERROR] No se pudo actualizar los repositorios.${NC}"
  exit 1
fi

# Comprobar si git está instalado
echo -e "${YELLOW}Comprobando si git está instalado...${NC}"
if ! command -v git &> /dev/null; then
  echo -e "${RED}[AVISO] git no está instalado. Instalando git...${NC}"
  if apt-get install -y git; then
    echo -e "${GREEN}[OK] git instalado correctamente.${NC}"
  else
    echo -e "${RED}[ERROR] No se pudo instalar git.${NC}"
    exit 1
  fi
else
  echo -e "${GREEN}[OK] git ya está instalado.${NC}"
fi

# Clonando el repositorio de CUPP
echo -e "${YELLOW}Clonando el repositorio de CUPP...${NC}"
if git clone https://github.com/Mebus/cupp.git /opt/cupp; then
  echo -e "${GREEN}[OK] Repositorio clonado en /opt/cupp.${NC}"
else
  echo -e "${RED}[ERROR] No se pudo clonar el repositorio.${NC}"
  exit 1
fi

# Crear enlace simbólico para facilitar el uso
echo -e "${YELLOW}Creando un enlace simbólico para CUPP...${NC}"
if ln -sf /opt/cupp/cupp.py /usr/local/bin/cupp; then
  chmod +x /usr/local/bin/cupp
  echo -e "${GREEN}[OK] Enlace simbólico creado. Puedes ejecutar CUPP con el comando 'cupp'.${NC}"
else
  echo -e "${RED}[ERROR] No se pudo crear el enlace simbólico.${NC}"
  exit 1
fi

# Finalización
echo -e "${BLUE}##############################################${NC}"
echo -e "${GREEN}[ÉXITO] CUPP se ha instalado correctamente.${NC}"
echo -e "${BLUE}##############################################${NC}"
echo -e "${YELLOW}Para usar CUPP, simplemente ejecuta: ${NC}${GREEN}cupp${NC}"
echo -e "${YELLOW}Repositorio oficial: ${NC}${BLUE}https://github.com/Mebus/cupp${NC}"
