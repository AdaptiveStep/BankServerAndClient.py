# Client för socket server
# INIT Lab för programmeringsparadigm nov 2015
# Författare: Hariz Hasecic
# Kontakt : hariz@kth.se

import socket
import sys,time
from os import listdir

host = "localhost"    													# Global variabel
if len(sys.argv) > 1:													# What does this do?
	host = sys.argv[1]
	#
class Language():
	def __init__(self):
		self.STRINGS = []												# all the translated phrases will be stored here, and used as a "pseudo dictionary"
		self.possiblelangs =listdir(path="languages")  					# If you add more languages make sure to add the choices here. Server must also be adjusted.
		self.possiblelangs.sort()
	def setLang(self,language):											# loads a text file with all the strings and sets the language for the meny.
		filename = str("languages\\") + str(language)+".txt"
		infil = open(filename,'r')

		self.STRINGS
		self.STRINGS = []												#resets the string list

		for line in infil.readlines():
			self.STRINGS.append(line.strip().split(sep="="))
		for i in range(len(self.STRINGS)-1):
			setattr(self,self.STRINGS[i][0],self.STRINGS[i][1])
		
		infil.close()

class Client():															# denna klass ger den aktuella clienten en massa instansvariabler från filer och/eller server
	def __init__(self):													# klassen är också ramverket för klienten. 
		self.userId = ""
		self.password = ""
		self.saldo = ""
		self.name = ""
		self.inloggmessage =""
		self.menymessage = ""
		self.loadLang()
	
	# def loadmess(self):												# All the pretty menu prints are here.
		# self.menymessage = ""
		# #Nedanstående fil kommer finnas på ett webhotell
		# #och kommer laddas i stil med:	# import urllib.request
		# 									# response = urllib.request.urlopen('http://minsajt.org/message.txt')
		# 									# infil = response.read()

		# infil = open("Message.txt",'r')
		# for line in infil.readlines():
		# 	self.menymessage += line
		# infil.close()
		# return self.menymessage
	
	def checkmess(self,message):										# This message checks to see if the message from the menu came trough to the server.
		if message == "offline":
			time.sleep(1)
			print(self.lang.stringcantcont)     						# string says that it cant connect
			if input(self.lang.stringtypeyes) == "yes":
				self.logon = False
				print(self.lang.stringloggedout) 						# String says it has logged out.	
			else:
				quit()
	def loadLang(self):
		self.lang = Language()											# creates the language instance-object, which is later used for changing language.
		self.lang.setLang("english") 									# Loads all the strings from selected file

	def menychoiceprint(self):
		self.menymessage = self.send_tcp("LB") 							#Loads the bottom banner from server.

		print("\n"+ self.lang.stringpleasemk + "\n\n"+
			self.lang.stringtodpstmon + "\n"+
			self.lang.stringmenuwithdraw + "\n"+
			self.lang.stringmenuchpass + "\n"+
			self.lang.stringmenubalance + "\n"+
			self.lang.stringmenuchlang + "\n"+
			self.lang.stringmenulogoff+
			"\n\n" + str(self.menymessage))
	def printcounter(self):             								# Shows a pretty counter
		print(" 3", end="",flush=True)
		time.sleep(0.3)
		print("2" ,end="",flush=True)
		time.sleep(0.2)
		print("1", end="",flush=True)
		time.sleep(0.1)
		print(". Continuing...\n")

	def menyn(self):													# Denna metod är huvudmetoden i clientprogrammet. Innehåller menyn som gör allt.
		self.logon = False
		while 1:
			if self.logon == True:
				#self.loadmess()											
				self.menychoiceprint()  								#prints all the menu stuff

				choice = input("\n" +self.lang.stringwhatwant)          #makes a choice and checks to see if choice is valid
		        
				if choice == "1":										#sätter in pengar
					message = self.send_tcp("D1")
					self.checkmess(message)								#checks to see if the menu choice was successful. Same for all the below.

				elif choice == "2":
					message = self.send_tcp("W1")
					self.checkmess(message)
				elif choice == "3":
					message = self.send_tcp("C1")
					self.checkmess(message)

				elif choice == "4":
					message = self.send_tcp("S1")
					self.checkmess(message)

				elif choice == "5":
					message = self.send_tcp("CL")
					self.checkmess(message)

				elif (choice == "99"):
					message = user.send_tcp("LO")
					print("\n" + self.lang.stringloggedout + "\n")
					time.sleep(0.3)
					self.logon = False
				else:
					print("\n"+self.lang.stringinvalid + "\n")
					self.printcounter()
			else:
				print("********************************"+"\n == Bankomat 2000 == \n")
				if user.connection() != "offline":
					message = user.send_tcp("LI")

				if message == "ok":
					self.logon = True
				elif message == "offline":
					time.sleep(1)
					print(self.lang.stringcantcont)
					if input(self.lang.stringtypeyes) != "yes":
						break
				elif message =="DE":
					print(self.lang.stringaccdeni)
					self.printcounter()
				else:
					print("\n "+self.lang.stringwronglog+"\n ")
					
	######################NO MORE MENY ###################################################################
	def trysend(self, message):											# This function makes sure that all messages are properly sent #if the message fails, or if connection breaks, offline message will show
		try:
			self.netock.send(bytes(message,"UTF-8"))
		except:
			print("Message failed to send")
			return "offline"
	def tryrecv(self):													# This method tries to recieve a message and decode it into a normal string
		try:
			return bytes.decode(user.netock.recv(512))
		except:
			return "offline"
	######################NO MORE TRYIERS ################################################################
	def connection(self):
		my_port = 13134   # hardcoded
		print(self.lang.stringtryingtoconnect)
		time.sleep(0.2)
		try:
			user.netock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET tillhör pythons inbyggda socket klass och behöver alltid skrivas vid skapande av de inbyggda socket objekten
																			# dvs socket.AF_INET returnerar: <AddressFamily.AF_INET: 2> . Dvs ett AdressFamily objekt.
			user.netock.connect((host, my_port))							#host = localhost , my_port = 13134

			print(self.lang.stringconest)
		except:
			print(self.lang.stringseemsunav)
	def feedreciever(self):
		# tempstring = ""
		# while 1:
		# 	temp2 = self.tryrecv()
		# 	if temp2 == "#":break
		# 	elif temp2=="offline": return temp2
		# 	else:
		# 		tempstring += temp2
		# 		trysend = self.trysend("Y")
		# 		if trysend == "offline": return trysend
		# return tempstring
		response = self.tryrecv()
		if response =="offline": return response
		return response

	def feedsender(self,astring):
		# for i in astring:  # Sending one character at the time
		# 	self.trysend(i)
		# 	confirm = self.tryrecv()
		# 	if confirm == "Y":  # This is expected from klienten to confirm that package has been recieved.
		# 		continue
		# 	elif confirm =="offline": return "offline"
		# 	else:
		# 		break
		# self.trysend("#")
		response = self.trysend(astring)
		if response =="offline": return response

	def send_tcp(self, message):    									# This method cordinates the client socket logic, it connects the menu and the socket stuff, i.e it makes sure everything gets sent.

		self.feedsender(message)										#connects and sends action signature to server.
		if message == "LI": 											#Checks to see if the user wants to login simoultanously as the server does his part.
			while 1:
				userId = input("\n UserId: ")
				password = input(" Password: " )

				if userId =="" or password=="":
					print(self.lang.stringwrongin)
					continue           									#if the user enters empty details. He just gets to re-enter them.
				
				if (self.feedsender(userId) == "offline" or self.feedsender(password) == "offline"):
					print(self.lang.stringqantquery)
					return "offline"
				else:
					answer = self.feedreciever()

					if answer == "ok":
						inlogmsg = self.feedreciever()

						self.userId = userId
						self.password = password
						self.printcounter()
						print(self.lang.stringloginsucess)
						time.sleep(0.2)

						print(inlogmsg)
						return answer
						break
					elif answer == "DE":
						print("\n",self.lang.stringaccdeni)     	#I have two of these now, remove one.
						self.feedsender(message)              #If the user enters wrong details, the server gets to know he wants to log in again.
						self.printcounter()
						continue
					else:
						break
		elif message == "D1":											#Checks to see if user wants to deposit money.

			answer = self.feedreciever()
			while 1:
				if answer == "HM":
					try:
						cash = input(self.lang.stringdeposhowmuch)
						int(cash)
						self.feedsender(cash)
						answer2 = self.feedreciever() 					#Is supposed to recieve "ok"
					except:
						print(self.lang.stringnotnumber, "\n")
						answer2="wrong"				  					#Internt meddelande ifall man ej anger ett tal
						time.sleep(0.2)
						continue
					if answer2 == "ok":
						print(self.lang.stringdeposited, int(cash))
						time.sleep(0.3)
						return
						break
					else:
						print(self.lang.stringsomwrong)
						time.sleep(0.3)
						self.feedsender("offline")
						return "offline"
						break
				else:
					print(self.lang.stringsomwrong) 					#If the client doesn't understand the message recieved it tells so.
					time.sleep(0.3)
					return "offline"
					break
		elif message == "W1":    										#works a little as the else clause above: Warning, code repitition.. Will fix it later with a "modify function" that just sends a negative value.
			answer = self.feedreciever()
			while 1:
				if answer == "HM":

					howmuch = input(self.lang.stringhwmuchw)
					
					if howmuch =="":
						print(self.lang.stringhavetotype)
					elif int(howmuch)==0:
						self.feedsender("offline") 						#This works as sending the "Aborted" message
						return
					else:
						ticket = input("  ticket -> ") 					#Fråga endast efter ticket ifall uttag större än 0 görs.
						self.feedsender(howmuch)
						self.feedsender(ticket)
						answer2 = self.feedreciever()
						if answer2 == "ok":
							print(self.lang.stringyouwith, howmuch)
							self.printcounter()
							return
							break
						elif answer2 == "2M":
							print(self.lang.stringyoucant)				#Will later add string to show how much cash the user has.

						elif answer2 == "WT":							#Om användare skriver fel ticket, så printas bara Felticket meddelande.
							print(self.lang.stringwrongtick)
							return "offline"
						else:
							print(self.lang.stringsomwrong)
							return "offline"
				else:
					print(self.lang.stringsomwrong) 					#If the client doesn't understand the message recieved it tells so.
					time.sleep(0.3)
					return "offline"
					break
		elif message == "C1":
			answer = self.feedreciever()
			while 1:
				if answer =="2W":
					newpass = input(self.lang.stringwhapass)
					self.feedsender(newpass)
					answer2 = self.feedreciever()
					if answer2 =="ok":
						print(self.lang.stringchanpas, newpass)
						self.printcounter()
						return
						break
					elif answer2=="DE":
						print(self.lang.stringnewpass)
						return "offline"

					else:
						print(self.lang.stringsomwrong)	 				#This phrase and the next one repeats itself, put it in a method for shorter code.
				else:
					print(self.lang.stringsomwrong) 					#If the client doesn't understand the message recieved it tells so.
					time.sleep(0.3)
					return "offline"
					break
		elif message == "S1":
			answer = self.feedreciever()
			while 1:
				if answer != "offline":
					cash = answer
					print(self.lang.stringyouhavec, cash, self.lang.stringonaccount)
					input(self.lang.stringcontinue)
					return
					break

				else:
					print(self.lang.stringsomwrong) 					#If the client doesn't understand the message recieved it tells so.
					time.sleep(0.3)
					return "offline"
					break
		elif message == "CL":
			#print(self.lang.stringlangchos)
			print("\n")     
			counter = 0
			
			for i in self.lang.possiblelangs:       					#prints all the possible choices
				counter +=1
				print(counter,":", i[:-4], "\n")
			try:
				val = input("Choice: ")
				val = int(val)-1
				sendlang =str(self.lang.possiblelangs[val][:-4])  		#creates a string without the ".txt" out of the choice
				val = str(val)
				self.feedsender(val)
				# self.trysend(val)

				print(sendlang, "!!")
				self.printcounter()
				self.lang.setLang(sendlang)
				return
			except:
				print("Error.")
				self.printcounter()
				return
		elif message =="LB":
			answer = self.feedreciever()
			if answer != "offline":
				menymessage = answer
				return menymessage
			else:
				print(self.lang.stringsomwrong) 						#If the client doesn't understand the message recieved it tells so.
				time.sleep(0.3)
				return "offline"
		else:
			answer="offline"
			return answer
		user.netock.close()
		return answer
	######################END OF TCP_SEND ###############################################################
	def main(self):
		user.menyn()
		#

user = Client()
user.main()

try:
	input("\n " + myserv.lang.stringanykey)
except:
	input("\n Type anything to exit: ")