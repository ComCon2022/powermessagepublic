#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import tkinter
import os
try:
	import cryptocode
except:
	print("Fatal Error! Failed to get required libs. Error note: Please install Cryptocode using 'pip install cryptocode'")
import time
import sys
from tkinter import messagebox

print("WARNING! THIS IS A DEVELOPER BUILD AND MAY NOT BE STABLE!")

def receive(event=None):
	oldmsg = ""
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode("utf8")
			decoded = cryptocode.decrypt(msg, PASS)
			# msg_list.insert(tkinter.END, decoded)
			if not decoded == oldmsg:
				print(decoded)
			oldmsg = decoded
		except OSError:  # Client Side Exited Out
			break
def send(event=None):
	while True:  
		sendmsg = input()
		if "fr:" in sendmsg:
			preparedsendingmessage = sendmsg
		else:
			preparedsendingmessage = "gb:" + sendmsg
		encoded = cryptocode.encrypt(preparedsendingmessage, PASS)
		if not len(encoded) > 1000:
			client_socket.send(bytes(encoded, "utf8"))
			client_socket.send(bytes(encoded, "utf8"))
		else:
			print("Message too long!")
		if sendmsg == "/quit":
			client_socket.close()
			quit()

global PASS
global client_socket
global BUFSIZ

HOST = input("HOST: ")
PORT = input("PORT: ")
PASS = input("PASS: ")

if not PORT == "":
	if not PORT.isdigit() or int(PORT) > 65535:
		messagebox.showerror("Invaild Port", "The port you entered is invaild. The default port for PowerMessage is 33000. You either entered a port that does not contain strictly integers or you entered a port that is greater than the port range 0-65535.")
		exit()
if not PORT:
	PORT = 33000
else:
	PORT = int(PORT)
BUFSIZ = 4096
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
result = client_socket.connect_ex(ADDR)
if result == 0:
	print("Server found, attempting to connect...")
else:
	print("Unable to resolve IP (hostname) and/or port is unreachable. Your IP or Port must be wrong or a server is not running behind that address.")
	client_socket.close()
	messagebox.showerror("Unable to Locate Server", "Unable to resolve IP (hostname) and/or port is unreachable. Your IP or Port must be wrong or a server is not running behind that address.")
	exit()
client_socket.send(bytes(PASS, "utf8"))
passcheck = False
while passcheck == False:
	if client_socket.recv(BUFSIZ).decode("utf8") == "true":
		passcheck = True
	else:
		print("Authentication Failed")
		client_socket.close()
		messagebox.showwarning("Authentication Failed", "Authentication Failed. The server has declined your password.")
		exit()
print("Successfully Connected")

SOLI = input("[S/L] Sign-up or Login")

if SOLI == "S":
	NUSER = input("User: ")
	NPASS = input("Pass: ")
	SIGNCRED = ("SP:" + NUSER + ":" + NPASS)
	client_socket.send(bytes(SIGNCRED, "utf8"))
if SOLI == "L":
	NUSER = input("User: ")
	NPASS = input("Pass: ")
	SIGNCRED = ("LN:" + NUSER + ":" + NPASS)
	client_socket.send(bytes(SIGNCRED, "utf8"))
	print(client_socket.recv(BUFSIZ).decode("utf8"))
	client_socket.send(bytes("recvuser", "utf8"))

client_socket.send(bytes("ready", "utf8"))
	
receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
receive_thread.start()
send_thread.start()