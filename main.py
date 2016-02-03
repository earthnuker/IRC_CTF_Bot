import socket
import getpass
import shelve
import importlib
import time
import os
active_ctfs={}

def recvall(sock):
	data=""
	while True:
		chunk=str(sock.recv(4096),"utf-8")
		data+=chunk
		if data.endswith("\n"):
			return data.splitlines()

def send(sock,data,verbose=True):
	if verbose:print(">",data)
	return sock.send(bytes(data,"utf-8")+b"\n")

class CTF(object):
	def __init__(self,player,category):
		self.module=importlib.import_module("ctf_{}".format(category))
		self.player=player
		self.level=1
		self.score=0
		self.load()
	
	
	def load(self):
		modname="Level_{}".format(self.level)
		if hasattr(self.module,modname):
			self.challenge=self.module.__getattribute__(modname)()
		else:
			return True
	
	def verify(self,ans):
		ok=self.challenge.verify(ans)
		if ok:
			self.level+=1
			self.score+=self.challenge.points
		return ok
	
	def get(self):
		return self.challenge.text.format(self.challenge.challenge)
	
	def hint(self):
		return self.challenge.hint
	
class Commands(object):
	def __init__(self,bot):
		self.commands=[cmd for cmd in dir(self) if cmd.startswith("cmd_")]
		self.bot=bot
		self.admins=[self.bot.owner]
	
		
	def cmd_help(self,command=None):
		return ["CTF-Bot very early version"]
	
	def cmd_start(self,category='crypto'):
		player=self.bot.lastmsg['src_nick']
		try:
			ctf_inst=CTF(player,category)
		except Exception as e:
			return ["Error: {}".format(str(e))]
		if not player in active_ctfs:
			active_ctfs[player]=ctf_inst
			ret=["Starting CTF with "+self.bot.lastmsg['src_nick']+", Category is "+category,
				active_ctfs[player].get()]
		else:
			ret=[self.bot.lastmsg['src_nick']+" is already doing a ctf with category "+category]
		print(ret)
		return ret
	
	def cmd_hint(self):
		player=self.bot.lastmsg['src_nick']
		return [active_ctfs[player].hint()]
	
	def cmd_quest(self):
		player=self.bot.lastmsg['src_nick']
		return [active_ctfs[player].get()]
	
	def cmd_ans(self,ans):
		player=self.bot.lastmsg['src_nick']
		if active_ctfs[player].verify(ans):
			if active_ctfs[player].load():
				return ["Congratulations, you've completed the CTF","Your final score is: {}".format(active_ctfs[player].score)]
		return ["Well Done!",active_ctfs[player].get()]
	
	def default(self,item,*args):
		return
	
	def __call__(self,item,args):
		try:
			return self.__getattribute__("cmd_"+item)(*args)
		except Exception as e:
			print("Error: ",e)
			return ["Error: "+str(e)]
	
class IRCBot(object):
	def __init__(self):
		self.trigger="!"
		self.server="irc.bonerjamz.us"
		self.port=6667
		self.channels=['#tuug']
		self.nick="CryptoCTF-Bot"
		self.owner="Earthnuker"
		self.execute=Commands(self)
		self.password=getpass.getpass("Password:")

	def run(self):
		initial_commands=[
			"USER {} {} {} {}".format(self.nick,self.nick,self.nick,self.owner),
			"NICK {}".format(self.nick),
			"PRIVMSG NickServ :identify {} {}".format(self.owner,self.password),
		]+["JOIN {}".format(channel) for channel in self.channels]
		self.irc_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.irc_socket.connect((self.server,self.port))
		self.irc_server=self.irc_socket.getpeername()
		print("Connected to {}:{}".format(*self.irc_server))
		for cmd in initial_commands:
			send(self.irc_socket,cmd)
			for message in recvall(self.irc_socket):
				self.process(message)
		while 1:
			for message in recvall(self.irc_socket):
				self.process(message)
	
	def terminate(self,msg):
		if msg:
			send(self.irc_socket,"QUIT {}".format(msg))
		else:
			send(self.irc_socket,"QUIT Terminating")
		self.irc_socket.close()
		#self.db.close()
		exit(0)
		
	def process(self,message):
		if message.startswith(":"):
			src,msg_type,to,*cont=message[1:].split()
			src_nick=src.split("@")[0].split("!")[0]
		else:
			src=None
			to=None
			msg_type,*cont=message.split()
		cont=" ".join(cont)
		if cont and cont[0]==":":
			cont=cont[1:]
		if not msg_type in ["PING","372","373","375","005"]: # hide PING and MOTD
			print(message)
		if msg_type=="PING":
			send(self.irc_socket,"PONG {}".format(cont),False)
		if msg_type=="PRIVMSG":
			print("[{}] {}: {}".format(time.ctime(),src.split("!")[0],cont))
			if to in self.channels+[self.nick]:
				if cont[0]==self.trigger:
					args=cont.split(" ")
					command=args[0][len(self.trigger):]
					self.lastmsg={"src_nick":src_nick,"src":src,"type":msg_type,"to":to,"cont":cont}
					ret=self.execute(command,args[1:])
					if ret:
						if to==self.nick:
							to=src.split("!")[0]
						for rv in ret:
							print(ret)
							send(self.irc_socket,"PRIVMSG {} :{}".format(to,rv))
try:
	Bot=IRCBot()
	Bot.run()
except Exception as e:
	#Bot.terminate(str(e))
	raise