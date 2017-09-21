#encoding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import socket,os,eyed3, unicodedata,threading,time,subprocess
from os import listdir
from os.path import isfile, join

class Server(threading.Thread):
	def __init__(self):
		self.segue = True
		threading.Thread.__init__(self)
		self.mypath = "D:\Musicas\Musicas"
		self.XmPlayPath = "..\\..\\xmplay\\xmplay.exe"
		self.carrega()
		if self.checkXm() ==  False:
			print "Xmplay nao iniciado"
			print "Iniciando..."
			os.system("start "+self.XmPlayPath)
			print "Xmplay iniciado"

		HOST = '0.0.0.0'              # Endereco IP do Servidor
		PORT = 7000            # Porta que o Servidor esta
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		orig = (HOST, PORT)
		self.udp.bind(orig)

		self.availableCommands = [
			'play',
			'pause',
			'vm-up',
			'vm-dw',
			'stop',
			'back',
			'next',
			'random',
			'eq-tg',
		]

		self.actualCommands = [
			'DDE_run -s XMPlay -t System -c key80',
			'DDE_run -s XMPlay -t System -c key80',
			'DDE_run -s XMPlay -t System -c key512',
			'DDE_run -s XMPlay -t System -c key513',
			'DDE_run -s XMPlay -t System -c key81',
			'DDE_run -s XMPlay -t System -c key129',
			'DDE_run -s XMPlay -t System -c key128',
			'DDE_run -s XMPlay -t System -c key130',
			'DDE_run -s XMPlay -t System -c key516',
			
		]
	
	def queue(self,arg):
		
		os.system('DDE_run -s XMPlay -t System -c key340')
		os.system('DDE_run -s XMPlay -t System -c key342')
		os.system('DDE_run -s XMPlay -t System -c key370')
		
		os.system("start "+self.XmPlayPath+"  -list \""+self.mp3only[arg-1][1]+"\"")
		
		os.system('DDE_run -s XMPlay -t System -c key340')
		os.system('DDE_run -s XMPlay -t System -c key337')
		os.system('DDE_run -s XMPlay -t System -c key374')
		
		os.system("start "+self.XmPlayPath+"  -list \""+self.mypath+"\"")
		
	
	def go(self,url):
		driver = webdriver.Chrome()
		driver.get("http://convert2mp3.net/en/")
		driver.find_element_by_name("url").send_keys(url)
		driver.find_element_by_xpath("//*[@id=\"convertForm\"]/fieldset/button").click()
		while len(driver.window_handles) > 1:
			driver.switch_to_window(driver.window_handles[1])
			driver.close()
		driver.switch_to_window(driver.window_handles[0])
		driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/form/div[5]/div/a").click()
		href = driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div[2]/div[2]/a[1]").get_attribute("href")
		driver.close()
	
		return href
	
	def goYou(self,termo):
		try:
			driver = webdriver.Chrome()
			driver.get("http:\\google.com")
			driver.find_element_by_xpath('//*[@id="lst-ib"]').send_keys(termo)
			driver.find_element_by_xpath('//*[@id="lst-ib"]').send_keys(Keys.ENTER)
			driver.find_element_by_xpath('//*[@id="hdtb-msb-vis"]/div[2]/a').click()
			
			urls = driver.find_elements_by_class_name("_Rm")
			
			for i in urls:
				if 'youtube.com' in i.text:
					url = i.text
					break
			driver.close()
			return self.go(url)
		except Exception as ex:
			print ex
			try:
				driver.close()
			except:
				pass
	
	def checkXm(self):
		s = subprocess.check_output('tasklist', shell=True)
		
		return "xmplay.exe" in s

	def send_commands(self,cliente):
		HOST = cliente[0]  # Endereco IP do Servidor
		PORT = 7060            # Porta que o Servidor esta
		udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		dest = (HOST, PORT)
		comands = self.availableCommands
		comands += ['play #','quit','charge','commands','help','busca','busca youtube','queue #']
		udp.sendto ("start", dest)
		udp.sendto ("#### Os comandos disponiveis são: ####", dest)
		for i in comands:
			try:
				udp.sendto (i, dest)
				time.sleep(0.1)
			except:
				pass
		udp.sendto ("EOF", dest)
		udp.close()

	def carrega(self):
			
		onlyfiles = [f for f in listdir(self.mypath) if isfile(join(self.mypath, f)) and ".mp3" in f]
		self.mp3only = []
		
		for i in onlyfiles:
			try:
				tag = eyed3.core.load(self.mypath+"\\"+i).tag
				if tag.title:
					if tag.artist:
						self.mp3only.append([unicodedata.normalize('NFKD', tag.title).encode('ascii', 'ignore') + " - " +unicodedata.normalize('NFKD',tag.artist).encode('ascii','ignore')] + [ self.mypath+"\\"+i])
					else:
						self.mp3only.append([unicodedata.normalize('NFKD', tag.title).encode('ascii', 'ignore')] + [self.mypath+"\\"+i])
				else:
					print i
					self.mp3only.append([unicodedata.normalize('NFKD',i.decode('utf-8')).encode('ascii', 'ignore')] + [self.mypath+"\\"+i])
			except:
				pass
			
		self.mp3only.sort()
		
		for i in range(len(self.mp3only)):
			self.mp3only[i][0] = str(i+1) + " - " + self.mp3only[i][0]
		
		self.mp3only.append(["EOF","EOF"])
		print "Done!"

	def lista(self,cliente):
		HOST = cliente[0]  # Endereco IP do Servidor
		PORT = 7060            # Porta que o Servidor esta
		udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		dest = (HOST, PORT)
		udp.sendto ("start", dest)
		for i in self.mp3only:
			try:
				udp.sendto (i[0], dest)
				time.sleep(0.01)
			except:
				pass
		udp.close()
		
	def play(self,arg):
		print self.XmPlayPath+" -play "+self.mp3only[arg-1][1],"D:\\Musicas\\xmplay.exe -list "+self.mypath
		
		os.system("DDE_run -s XMPlay -t System -c key341")
		os.system("DDE_run -s XMPlay -t System -c key370")
		os.system("DDE_run -s XMPlay -t System -c key10")
		
		os.system("start "+self.XmPlayPath+"  -play \""+self.mp3only[arg-1][1]+"\"")
		while self.checkXm() == False:
			pass
		os.system("start "+self.XmPlayPath+"  -list \""+self.mypath+"\"")
		
	def playUrl(self,arg):
		print arg
		
		os.system("DDE_run -s XMPlay -t System -c key341")
		os.system("DDE_run -s XMPlay -t System -c key370")
		os.system("DDE_run -s XMPlay -t System -c key10")
		
		url = self.go(arg)
		
		print url
		
		os.system("start "+self.XmPlayPath+"  -play \""+url+"\"")
		
		while self.checkXm() == False:
			pass
		time.sleep(2)
		os.system("start "+self.XmPlayPath+"  -list \""+self.mypath+"\"")
		
	def playYou(self,arg):
		print arg
		
		os.system("DDE_run -s XMPlay -t System -c key341")
		os.system("DDE_run -s XMPlay -t System -c key370")
		os.system("DDE_run -s XMPlay -t System -c key10")
		
		url = self.goYou(arg)
		
		print url
		
		os.system("start "+self.XmPlayPath+"  -play \""+url+"\"")
		
		while self.checkXm() == False:
			pass
		time.sleep(2)
		os.system("start "+self.XmPlayPath+"  -list \""+self.mypath+"\"")
	
	def search(self,arg,cliente):
		HOST = cliente[0]  # Endereco IP do Servidor
		PORT = 7060            # Porta que o Servidor esta
		udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		dest = (HOST, PORT)
		udp.sendto ("start", dest)
		for i in self.mp3only:
			if arg.lower() in i[0].lower():
				try:
					udp.sendto (i[0], dest)
					time.sleep(0.01)
				except:
					pass
		udp.sendto ("end", dest)
		udp.close()
		
	
	def run(self):
		while self.segue:
			try:
				self.udp.settimeout(1)
				msg, cliente = self.udp.recvfrom(1024)
				print msg
				print cliente[0]
				
				if 'play' in msg.lower() and len(msg.lower()) > 5:
					
					try:
						num = int(msg.lower()[4:].strip())
						self.play(num)
					except:
						self.playUrl(msg[4:])
				elif msg.lower() == 'charge':
					self.carrega()
				elif msg.lower() == 'list':
					self.lista(cliente)
				elif 'busca ' in msg.lower() and 'youtube' not in msg.lower():
					self.search(msg[6:],cliente)
				elif 'busca ' in msg.lower() and 'youtube' in msg.lower() :
					self.goYou(msg[14:])
				elif 'queue ' in msg.lower():
					try:
						num = int(msg.lower()[5:])
						self.queue(num)
					except:
						pass
				elif msg.lower() == "quit":
					os.system("DDE_run -s XMPlay -t System -c key10")
					self.para()
				elif msg.lower() in ['commands','help']:
					self.send_commands(cliente)
				else:
					for i in range(len(self.availableCommands)):
						if msg.lower() == self.availableCommands[i].lower():
							os.system(self.actualCommands[i])
			except Exception as inst:
				pass
	def para(self):
		self.segue = False
		self.udp.close()
	

