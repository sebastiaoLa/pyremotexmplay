#encoding: utf-8
import socket,threading

class Th(threading.Thread):
	def __init__(self):
		self.go = True
		threading.Thread.__init__(self)
		HOST = '0.0.0.0'              # Endereco IP do Servidor
		PORT = 7060            # Porta que o Servidor esta
		self.udp2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		orig = (HOST, PORT)
		self.udp2.bind(orig)

	def run(self):
		while self.go:
			try:
				self.udp2.settimeout(1)
				msg, cliente = self.udp2.recvfrom(1024)
				if msg != "EOF":
					print msg
			except:
				pass
		
	def stop(self):
		self.go = False

th = Th()
th.start()
HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 7000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
print 'Para sair use CTRL+X\n'
msg = raw_input()
while msg <> '\x18':
	udp.sendto (msg, dest)
	msg = raw_input()

th.stop()
udp.close()
