#!/usr/bin/python
import sys
import os
import subprocess
import socket

found = False
while not found:
	try:
		ifconfig_list = subprocess.check_output("ifconfig eth0; exit 0", stderr = subprocess.STDOUT, shell = True )
		ifconfig_list = ifconfig_list.split('\n')
		inet_list = ifconfig_list[1].strip().split()
		if inet_list[0].strip() == "inet":
			found = True
	except Exception:
		inet_list = ["poop","poop","poop"]
		continue
addr = inet_list[1].strip('addr:')


server = '129.25.35.152'
port = 21210

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect( (server, port) )
count = 0
sock.sendall(addr)
sock.close()
