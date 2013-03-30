
import logging
import os
import select
import socket
import sys
import threading
import traceback
import time

# Find the Script's Current Location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Set up Logging
logging.basicConfig(filename="/var/log/datamap.log",level=logging.DEBUG)

# General Configuration
MAX_MSG_SIZE = 1024
HEARTBEAT_INT = 1
TIMEOUT = 5
CONFIG_FILE = __location__ + "/.datamap_config"

# Central Server / Collection Node Messages
HELLO_MSG = "hello"
HEARTBEAT_MSG = "heartbeat"
NAME_MSG_PREFIX = "name:"
START_MSG = "start"
STOP_MSG = "stop"

# Central Server / Controller Messages
REMOVE_COMMAND_PREFIX = "remove"
START_COMMAND_PREFIX = "start"
STOP_COMMAND_PREFIX = "stop"
STATUS_MSG = "status"

# General Messages
ACK_MSG = "ack"
NACK_MSG = "nack"

# Gets the configuration value associated with the provided name
def get_config(name):
	file = open(CONFIG_FILE,"r")
	contents = file.read()
	lines = contents.split("\n")
	for line in lines:
		if (line.startswith(name+"=")):
			return line.replace(name+"=","").strip()
	logging.error("Failed to find configuration item \"" + name + "\"")
	return None

# Sends the supplied message to the specified address on the specified port. Returns None if successful, or an error message if not
def send_and_get_ack(addr, port, msg):
	logging.debug("Sending message \"" + msg + "\" to " + str(addr) + ":" + str(port) + " and expecting ACK.")
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((addr,port))
		sock.send(msg)
		ready = select.select([sock],[],[],TIMEOUT)
		if (ready[0]):
			reply = sock.recv(MAX_MSG_SIZE)
			sock.close()
			if (reply == ACK_MSG):
				return None
			else:
				return "Unexpected reply: " + reply
		else:
			return "Timed out waiting for ack from " + addr + ":" + str(port)
	except:
		return "Error occured while sending message to " + addr + ": " + str(sys.exc_info())

# Class that allows a looped thread to be stopped. It will run the init function provided in the constructor and then enter an infinite loop running the loop function until stop() is called. Then, the uninit function will be called after the next loop iteration finishes and before the thread exits.
class StoppableThread(threading.Thread):
	def __init__(self, init, loop, uninit):
		threading.Thread.__init__(self)
		self.init = init
		self.loop = loop
		self.uninit = uninit
	def run(self):
		self.init()
		self.done = False
		while not self.done:
			self.loop()
		self.uninit()
	def stop(self):
		self.done = True

# Class that listens on a socket and passes the messages back to a message handler
class ConnectionHandlerThread(StoppableThread):
	def __init__(self, addr, port, callback):
		StoppableThread.__init__(self, self.init, self.loop, self.uninit)
		self.addr = addr
		self.port = port
		self.callback = callback
	def init(self):
		self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.listen_socket.bind((self.addr, self.port))
		self.listen_socket.listen(10)
	def loop(self):
		try:
			ready = select.select([self.listen_socket],[],[],TIMEOUT)
			if (not ready[0]):
				return
			conn,addr = self.listen_socket.accept()
			ready = select.select([conn],[],[],TIMEOUT)
			if (ready[0]):
				msg = conn.recv(MAX_MSG_SIZE).strip()
				self.callback(conn,addr,msg)
			else:
				logging.warn("Recieve timout")
			conn.close()
		except:
			logging.error("An error occured when recieving: " + str(sys.exc_info()))
			traceback.print_exc()
	def uninit(self):
		self.listen_socket.shutdown(socket.SHUT_RDWR)
		self.listen_socket.close()