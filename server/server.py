#encoding: utf-8

import socket,os,eyed3, unicodedata,threading,time,subprocess
from os import listdir
from os.path import isfile, join

mypath = "D:\Musicas\Musicas"

def checkXm():
	s = subprocess.check_output('tasklist', shell=True)
	
	return "xmplay.exe" in s

def carrega():
	global mp3only
	
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and ".mp3" in f]
	mp3only = []
	
	for i in onlyfiles:
		try:
			tag = eyed3.core.load(mypath+"\\"+i).tag
			if tag.title:
				if tag.artist:
					mp3only.append([unicodedata.normalize('NFKD', tag.title).encode('ascii', 'ignore') + " - " +unicodedata.normalize('NFKD',tag.artist).encode('ascii','ignore')] + [ mypath+"\\"+i])
				else:
					mp3only.append([unicodedata.normalize('NFKD', tag.title).encode('ascii', 'ignore')] + [mypath+"\\"+i])
			else:
				print i
				mp3only.append([unicodedata.normalize('NFKD',i.decode('utf-8')).encode('ascii', 'ignore')] + [mypath+"\\"+i])
		except:
			pass
		
	mp3only.sort()
	
	for i in range(len(mp3only)):
		mp3only[i][0] = str(i+1) + " - " + mp3only[i][0]
	
	mp3only.append(["EOF","EOF"])
	print "Done!"

def lista(cliente):
	global mp3only
	
	HOST = cliente[0]  # Endereco IP do Servidor
	PORT = 5060            # Porta que o Servidor esta
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dest = (HOST, PORT)
	
	for i in mp3only:
		try:
			udp.sendto (i[0], dest)
		except:
			pass
	udp.sendto ("EOF", dest)
	udp.close()
	
def play(arg):
	global mp3only,mypath
	print "D:\\Musicas\\xmplay.exe -play "+mp3only[arg-1][1],"D:\\Musicas\\xmplay.exe -list "+mypath
	
	os.system("DDE_run -s XMPlay -t System -c key341")
	os.system("DDE_run -s XMPlay -t System -c key370")
	os.system("DDE_run -s XMPlay -t System -c key10")
	
	os.system("start D:\\Musicas\\xmplay\\xmplay.exe  -play \""+mp3only[arg-1][1]+"\"")
	time.sleep(0.1)
	os.system("start D:\\Musicas\\xmplay\\xmplay.exe  -list \""+mypath+"\"")
	
	
carrega()
if checkXm() ==  False:
	print "Xmplay nao iniciado"
	print "Iniciando..."
	os.system("start D:\\Musicas\\xmplay\\xmplay.exe")
	print "Xmplay iniciado"

HOST = '0.0.0.0'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)

availableCommands = [
	'play',
	'pause',
	'volume-up',
	'volume-down',
	'stop',
	'back',
	'next',
	'random',
]

actualCommands = [
	'DDE_run -s XMPlay -t System -c key80',
	'DDE_run -s XMPlay -t System -c key80',
	'DDE_run -s XMPlay -t System -c key512',
	'DDE_run -s XMPlay -t System -c key513',
	'DDE_run -s XMPlay -t System -c key81',
	'DDE_run -s XMPlay -t System -c key129',
	'DDE_run -s XMPlay -t System -c key128',
	'DDE_run -s XMPlay -t System -c key130',
]


while True:
	msg, cliente = udp.recvfrom(1024)
	print msg
	print cliente[0]
	
	if 'play' in msg.lower() and len(msg.lower()) > 5:
		play(int(msg.lower()[4:].strip()))
	elif msg.lower() == 'charge':
		carrega()
	elif msg.lower() == 'list':
		lista(cliente)
	elif msg.lower() == "quit":
		os.system("DDE_run -s XMPlay -t System -c key10")
		exit()
	else:
		for i in range(len(availableCommands)):
			if msg.lower() == availableCommands[i].lower():
				os.system(actualCommands[i])
    
udp.close()
