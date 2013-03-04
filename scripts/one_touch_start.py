#!/usr/bin/python

import sys
import os
import time
import subprocess
import socket
import select

def run_select(server_sock, sock_list):
    selectUnsuccessful = True
    while selectUnsuccessful:
        try:
            readyRecvList, readySendList, readyErrList = select.select( sock_list, [], [], 20 )
            selectUnsuccessful = False
        # select error handler
        except select.error:
            for fd in sock_list:
                try:
                    tempRecvList, tempSendList, tempErrList = select.select( [ fd ], [], [], 0 )
                except select.error:
                    if ( fd == server_sock ):
                        fd.close()
                        exit( 1 )
                    else:
                        if fd in sock_list:
                            sock_list.remove( fd )
                        fd.close()

    return readyRecvList

def listener( server_sock, sock_list ):
	try:
		conn, addr = server_sock.accept()
	except socket.error:
		print "Socket Error at listener Top"
		exit(-1)

	sock_list.append( conn )
	# msg = str(addr) + " has joined the channel"
	return sock_list

def receive( sock, sock_list, node_list ):
	try:
		rmsg = sock.recv( 1024 )
		node_list.append( rmsg )
		print "Currently connected but not 'start'ed- "
		for i in node_list:
			print i
		#print 'hahahahahaha'
		print ''
		if sock in sock_list:
			sock_list.remove( sock )
		sock.close()
		return (sock_list, node_list)
	except socket.error:
		print "socket error in receive"
		if sock in sock_list:
			sock_list.remove( sock )
		sock.close()
		return (sock_list, node_list)

def get_stdin( std_in ):
	try:
		smsg = std_in.readline()
	except IOError:
		print "stdin error in send"
		smsg = "quit()"
	return smsg


def do_something( node_list, cmd ):
	print "Lets do work..."
	for ip in node_list:
		full_cmd = "ssh alix@" + ip + ' \'' + cmd + '\''
		#print "running command", full_cmd,"on: alix", item.split(',')[0]
		try:
			#print "herehased"
			p = subprocess.Popen(full_cmd, stderr = None, shell = True )
			# node_list.remove( item )
			#p.wait()
			#time.sleep(1)
			
		except Exception as err:
			print "something went wrong: ", err
			#return node_list
	#node_list = []
	return node_list

server = '129.25.35.152'
port = 21210
##########################################################
# CHANGE THIS LINE TO THE APPROPRIATE CMD TO BE EXECUTED #
##########################################################
command = 'echo s3tt0p! | sudo -S ~/DataMap/vermont/vermont -f ~/DataMap/vermont/db_config.xml -d'

server_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server_sock.setblocking( 0 )
server_sock.bind(( server, port ))
server_sock.listen(10)

node_list = []
sock_list = []
sock_list.append( server_sock )
sock_list.append( sys.stdin )
print "Starting Server..."
print "Once some nodes connect, you can type 'start' to start capturing on those nodes"

try:
	while True:
		ready_list = run_select( server_sock, sock_list )
		for i in ready_list:
			if i == server_sock:
				sock_list = listener( i, sock_list )
			else:
				if type (i) != socket.socket:
					std_in = get_stdin( i )
					print "ECHO: ", std_in
					if std_in == 'start\n':
						if len(node_list) > 0:
							node_list = do_something ( node_list, command )
						else:
							print "nodes have not responded yet"
							print "try again after you see some nodes connect"
				else:
					(sock_list, node_list) = receive ( i, sock_list, node_list )
except KeyboardInterrupt:
	print "exiting server"
	for ip in node_list:
		full_cmd = "ssh alix@" + str(ip) + " 'echo s3tt0p! | sudo -S killall vermont'"
		print full_cmd
		p = subprocess.Popen(full_cmd, stderr = None, shell = True )
		p.wait()

	for s in sock_list:
		s.close()
	exit(0)
