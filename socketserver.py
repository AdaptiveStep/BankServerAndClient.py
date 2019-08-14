														#SKAPAT AV HARIZ HASECIC, KTH (Copyright DECEMBER 2015)
														# Streamar en server, som en client kan ta kontakt med för att "ladda upp pengar".
														# Databasen för användare finns på en textfil, och nya översättningar kan skapas lätt. 
														# Tekniker som används är trådar och sockets. Maximal inkapsling och total objektorientering råder.
														#####################################################################################################

from os import listdir
import socket, threading, time, decimal      			# imports time to use for timing intervals, for saving everything to file.
class User():											# En hjälp class för att skapa databasen i minnet för servern
	def __init__(self):									# These are the main attribute for all users, they are loaded from the user.txt file
		self.id = 0
		self.name = ""
		self.password = ""
		self.saldo = 0
		self.usertype = ""
	def __str__(self):
		temp = "Användarnummer: " + str(self.id) + "\n" + "Namn: " + str(self.name) + "\nPassword: " + str(self.password) + "\nSaldo: " + str(self.saldo) + "\nUsertype: " + str(self.usertype)
		return temp
	def __repr__(self):
		return self.name
		#
class Mythread(threading.Thread): 		  				# subclass Thread object
	def __init__(self, conn, adress, mutex="None"):
		stdoutmutex = myserv.mutex        				# loads the threadlock from the "myserv object instance variable"
		local = self
		self.conn = conn
		self.adress = adress
		self.denied = True								# Makes sure that people who disconnect abruptly get correct message
		self.activate = True							# I forgot what this did..
		self.userIdobj = None
		self.mutexx = stdoutmutex         				# used for synchronizing the threads later on. Not sure how this works..
		threading.Thread.__init__(self)   				# inherits all the threading methods
	def feedsender(self,astring):
		# for i in astring:							#Sending one character at the time
		# 	response = myserv.trysend(self.conn, i)
		# 	if response == "offline":return "offline"
		# 	confirm = myserv.tryrecv(self.conn)
			
		# 	if confirm == "Y":						#This is expected from klienten to confirm that package has been recieved.
		# 		continue
		# 	elif confirm =="offline":
		# 		return "offline"
		# 	else:
		# 		break
		# myserv.trysend(self.conn, "#")				#This is always sent as a last character, to tell the client that feed is complete.
	

		response = myserv.trysend(self.conn, astring)
		if response == "offline": return "offline"
	def feedreciever(self): 							# Recieves one character at the time
		# tempstring = ""
		# while 1:
		# 	temp2 = myserv.tryrecv(self.conn)
		# 	if temp2 == "#":							#If it recieves this character, it means that the feed is complete.
		# 		break
		# 	elif temp2 =="offline":return "offline"
		# 	else:
		# 		tempstring += temp2
		# 		myserv.trysend(self.conn,"Y")
		# return tempstring
		response = myserv.tryrecv(self.conn)
		if response =="offline":return "offline"
		return response

	#THE MAIN METHOD OF THE SERVER
	def run(self):                  	  				# Run provides thread logic     #Not sure how to fix this..
		myserv.customers += 1 							# Visitors since the last restart.
		print(" New visitor! "+ 
			"Visitors since boot: ",myserv.customers)
		while self.userIdobj in myserv.usersonline or self.activate == True:  #A while loop is dedicated for every user that connects to the server.
			self.data = self.feedreciever() 			# recieves first signal from client, decides what he wants.
			if   self.data == "D1":				# checks to see if user wants to deposit
				print(myserv.get_id(self.userId).name, "wants to deposit. \n Sending request for sum..")

				self.feedsender("HM")
				self.cash = self.feedreciever()			#Tar emot summa som client skrivit in


				#self.cash = myserv.tryrecv(self.conn)
				if self.cash != "offline" :
					print("\t",myserv.get_id(self.userId).name,"deposited ", float(self.cash), end=" ")
					self.feedsender("ok")				#Besvarar client med "ok" sträng.
					myserv.get_id(self.userId).saldo = float(myserv.get_id(self.userId).saldo)+float(self.cash)
														##### OBS: ONLY SAVED TO ATTRIBUTE, NOT TO FILE. There is another loop later that saves all attributes to the file ######
				myserv.save()								# Saves everything from memory to file
			elif self.data == "W1":
				print(myserv.get_id(self.userId).name, "wants to withdraw money. \n Sending request for sum...")
				self.feedsender("HM")
				while 1:
					self.cash = self.feedreciever()					
				
					if self.cash != "offline":
						ticket = self.feedreciever()			#Tar emot ticket som client skrivit in
						try:
							self.cash = float(self.cash)	
							calc = float(myserv.get_id(self.userId).saldo) - float(self.cash)
						except:
							print(myserv.get_id(self.userId).name, "entered wrong ticket.")
							break					#will restart loop if not correct ticket is provided.
						if calc >= 0:
							myserv.get_id(self.userId).saldo = float(myserv.get_id(self.userId).saldo) - self.cash
							if ticket in myserv.tickets:
								self.feedsender("ok")
								myserv.tickets = myserv.tickets.difference({ticket})

								print(myserv.get_id(self.userId).name, "withdrew " + str(self.cash), end=" ")
								break
							else:
								self.feedsender("WT")

						elif calc < 0:
							# myserv.trysend(self.conn,"2much")
							self.feedsender("2M")
							print(myserv.get_id(self.userId).name, "tried to withdraw too much (" ,self.cash ,"). \n Sending error message. And another request for sum... ")
					else:
						print(myserv.get_id(self.userId).name, "broke the transaction.")
						break
				myserv.save()								# Saves everything from memory to file 
			elif self.data == "C1":	 				# this method follows the same model as the method above.
				print(myserv.get_id(self.userId).name, "wants to change password,\n Sending request for new pass...")
				self.feedsender("2W")
				while 1:
					self.newpass = self.feedreciever()
					if self.newpass != "offline" and self.newpass not in myserv.bannedwordlist:
						myserv.get_id(self.userId).password = self.newpass
						self.feedsender("ok")
						print("\t",myserv.get_id(self.userId).name, "changed his password to: " + str(self.newpass), end=" ")
						break
					elif self.newpass in myserv.bannedwordlist:
						self.feedsender("DE")
						print("\t",myserv.get_id(self.userId).name, "tried to change password to an unallowed phrase. Sending error message. And another request for sum... ")
					else:
						print("\t",myserv.get_id(self.userId).name, "wanted to change his password but failed. His password is still:", myserv.get_id(self.userId).password, ". The connection was lost.")
						break
				myserv.save()							# Saves everything from memory to file
			elif self.data == "CL":
				print(myserv.get_id(self.userId).name, "wants to change language. ")
				try:	
					choice = int(self.feedreciever())	#kan bli fel här så gör undantag
					print("\t", myserv.get_id(self.userId).name, " chose:", myserv.languages[choice])

				except:
					print("\t", myserv.get_id(self.userId).name,"provided wrong language choice.")
			elif self.data == "S1":
				print(myserv.get_id(self.userId).name, "wants to see his balance, (", float(myserv.get_id(self.userId).saldo) ,") granting access...")
				# myserv.trysend(self.conn,"ok")
				#self.feedsender("ok")
				self.feedsender(str(myserv.get_id(self.userId).saldo))   	   # sending a string of numbers.
			elif self.data == "LI":					# WARNING. COMPLICATED! Checks for correct login
				self.userId = self.feedreciever()							  	   #This block converts the userId 
				if self.userId != "offline":
					self.password = self.feedreciever()
				if self.userId != "offline" and self.password != "offline":   	  	   #if the self.userId and password is successfully recieved, we move on.
					for i in range(len(myserv.lista)):								   #tries to find the user in the database
						if myserv.lista[i].id == self.userId and myserv.lista[i].password == self.password:
							self.activate = False									   #After successful login, there is an thread attribute ".userIdobj" created and dedicated to the "user-object" found in the myserv list of possible users. 
							self.feedsender("ok")
							self.feedsender(myserv.readinlogmsg())

							myserv.id_set(self.userId)       													 #makes sure we get an object in the form myserv.id33 , where 33 is the userId
							self.userIdobj = myserv.get_id(self.userId)
							myserv.usersonline.append(myserv.get_id(self.userId))      							 #Always use the method get_id() to set the proper idnumber like "id33"

							print("The", myserv.lista[i].usertype , myserv.lista[i].name, "logged in.")
							print("There are now ",int(myserv.totalusers())-int(len(myserv.usersonline)), "guests and", len(myserv.usersonline),"registered users online:", myserv.usersonline)
							break
							
						elif myserv.lista[i].id == self.userId and myserv.lista[i].password != self.password:    #This will happen when the for loop has reached the last user
								myserv.id_set(self.userId)      												 #This creates an object that is used on the line below.
								userIdobj = myserv.get_id(self.userId)

								self.feedsender("denied")						    					 #When a recognized user is denied access. The server says so.
								print("Recognized user",userIdobj.name, "didn't access the server (Wrong password).")
								break
						elif i == (myserv.antalrader - 1) and myserv.lista[i].id != self.userId:				 #if the search is on the last element, and its not a recognized user. Then access is denied.
							print("Unknown user with userId", self.userId, "was denied acccess (wrong login).")
							self.feedsender("denied")
			elif self.data == "LO":
				print(myserv.get_id(self.userId).name, "has logged out.")
				myserv.usersonline.remove(self.userIdobj)
			elif self.data == "LB":
				#self.feedsender("ok")
				self.feedsender(myserv.readbannermsg())
			elif self.data == "offline":
				try:
					myserv.usersonline.remove(self.userIdobj)
					print(" ",self.userIdobj.name, "broke the connection abruptly.")
					break
				except:
					print("Unidentified user closed the client abruptly")
					break
		myserv.cleanthreadlist()    					# cleans the threadlist with "previous" users everytime someone disconnects. 
class Server():
	def __init__(self):
		self.threadlist = []							# All the threads will be in this list
		self.lista = []									# The "database" will be in this list
		self.bannedwordlist = [] 						# All the banned words will be stored in here. Used later for unallowed new usersnames and passwords.
		self.usersonline = []
		self.totalcashattr = 0

		self.customers = 0								# Total amount of visitors since the server went online
		self.antalrader = 0								# How many users are there in database?
		self.mutex = threading.Lock()					# This is used for thread synchronization
		
		my_port = 13134  								# hardcoded port
		self.netock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.netock.bind(("", my_port))
		self.netock.listen(5)
	def __str__(self):
		self.lista 										# just shows all the users possible.
		#
	def save(self):			   							# This method is used to update the actual list in the memory, and save everything to file.
		
		for element in self.lista:      				# Finds all the attributes (that are user objects) that are new, so that the list gets updated.
			if hasattr(self,"id"+element.id):			# Pretty complicated thing, don't think too much of this.
				ind = self.lista.index(element)
				self.lista[ind]=self.__getattribute__("id"+element.id)
		templist = []
		utfil = open('Users.txt','w')	
		for element in self.lista:						# saves all the users and their properties
			uttemp = str(element.id)+"##"+str(element.name)+"##"+str(element.password)+"##"+str(element.saldo)+"##"+str(element.usertype)+"\n"
			utfil.write(uttemp)
		utfil.close()
		
		ticketfil =open('tickets.txt','w')				#Saves the ticketsfile.
		for ticket in self.tickets:
			temp = ticket+"\n"
			ticketfil.write(temp)
		ticketfil.close

		print("\t\tDatabase is now updated. ")
	def msg(self):			   							# Loads the messages
		self.menumsginfil = open("Message.txt",'r') 	# opens all the files
		self.inlogmsginfil = open("inlogmessage.txt",'r')

		self.menumsg = ""
		for rad in self.menumsginfil.readlines():		# reads all the lines
			self.menumsg += rad         
		self.inlogmsg = ""
		for rad in self.inlogmsginfil.readlines():
			self.inlogmsg += rad

		self.menumsginfil.close()						# closes all the files
		self.inlogmsginfil.close()
	def totalcash(self):	    						# calculates the total amount of cash in the bank
		self.totalcashattr = 0
		for user in myserv.lista: self.totalcashattr += self.totalcashattr + float(user.saldo)
		return self.totalcashattr
	def storleksord(self):  							# Calculates storleksordningen for the total cash
		temp = decimal.Decimal(myserv.totalcash())
		temp = temp.logb()
		self.storleksordattr = int(temp)
		6 == self.storleksordattr
		return int(self.storleksordattr)
	def cashvolym(self):
		tempvol = self.storleksord()
		if tempvol >= 3 and tempvol <=4:
			self.cashvolym = "thousands" 				# 1000

		elif tempvol >= 4 and tempvol  <=5:				# 10 000
			self.cashvolym ="tens of thousands" 

		elif tempvol >= 5 and tempvol  <6: 				# 100 000
			self.cashvolym = "hundreds of thousands"

		elif tempvol >= 6 and tempvol  <9: 				# 1 000 000
			self.cashvolym = "millions"

		elif tempvol >= 9 and tempvol  <10: 			# 100 000 000
			self.cashvolym = "hundreds of millions"

		elif tempvol >= 10 and tempvol <11: 			# 1 000000000
			self.cashvolym = "billions"

		elif tempvol >= 11 and tempvol <12: 			# 100 000000000
			self.cashvolym = "hundreds of billions"

		elif tempvol >= 12: 							# 1000 000000000
			self.cashvolym = "gorillion"
		else: self.cashvolym = "magillions of gorillionss"
		return self.cashvolym
	def totalusers(self):
		return int(threading.active_count() -1)
		#
	def inlasning(self):       							# reads the user.txt database file
		self.msg() 										# This method reads all the message files.

		self.infil = open("Users.txt",'r')          	# Loads all the users
		run = True        
		for rad in myserv.infil:                    	# Läsloopen: ##  Denna skapar objekt från textfilen. Detta körs bara då programmet startar.
			nyttobj = User()                        	# skapar ett objekt för att sedan referrera det i en lista
			streng = rad
			strenglist = streng.strip().split(sep="##") # Ett objekt per loop. Varje split av raden ger värdet åt en instansvariabel.

			nyttobj.id = strenglist[0]              	# här byggs ett objekt upp så att det sedan kan läggas till i lista
			nyttobj.name = strenglist[1]
			nyttobj.password = strenglist[2]
			nyttobj.saldo = strenglist[3]
			nyttobj.usertype = strenglist[4]

			self.lista.append(nyttobj)     				# Lägger till varje objekt som byggts upp från ovan till serverns lista
			self.antalrader += 1           				# Räknar antalet rader i infilen, dvs antalet användare i databasen
		self.infil.close()          					# stänger infil efter att ha läst databasen
		
		self.languages = listdir(path="languages")    	# Loads all the language files for the client from directory "languages"
		counter = 0
		for langs in self.languages:
			self.languages[counter]=self.languages[counter][:-4]
			counter += 1

		self.readtickets()
	def id_set(self,idd):           					# creates an "user object" instance which is an object, every time someone logs in.
		radnummer = 0			    					# thus the instance myserv.id33 will be the object for the user with username 'ingvar kamprad'
		for i in range(len(self.lista)):
			if self.lista[i].id == idd:
				radnummer = i
		self.__setattr__(self.short_id(idd),self.lista[radnummer])
	def id_delete(self,idd):        					# This method is supposed to delete the attributes that got saved into the server object when the user logged in.This happens once the server has saved everything to database. It isn't used yet.
		self.__delattr__(self.short_id(idd))
		#
	def get_id(self,idd):	        					# this method is supposed to just show something like 
		temp = self.__getattribute__(self.short_id(idd))
		return temp
	def short_id(self,idd):        	 					# Just a "helper method" for shorter code. Helps the methods above, it returns something like id33 , where 33 is the self.userId.
		return "id{identitet}".format(identitet=idd)
		#  
	def trysend(self,conn, message):					# This function makes sure that all messages are properly sent #if the message fails, or if connection breaks, offline message will show
		try:
			conn.send(bytes(message,"UTF-8"))
		except:
			return "offline"
	def tryrecv(self,conn):		    					# This method tries to recieve a message and decode it into a normal string
		try:
			return bytes.decode(conn.recv(512))
		except:
			return "offline"
	     ######################NO MORE TRYERS#################################################
	def readtickets(self):
		self.tickets = frozenset()
		infil = open("tickets.txt",'r')
		for i in infil.readlines():
			self.tickets = self.tickets.union({i.strip()})
		infil.close()
	def readinlogmsg(self):
		infil = open("inlogmessage.txt",'r')
		self.inlogmsg =""
		for i in infil.readlines():
			self.inlogmsg += i
		infil.close()
		return self.inlogmsg
	def readbannermsg(self):
		infil = open("Message.txt",'r')
		self.bannermsg =""
		for i in infil.readlines():
			self.bannermsg += i
		infil.close()
		return self.bannermsg
	def online(self):
		while 1:
			self.client_socket, self.address = self.netock.accept()   # self.client_socket is used to send and recieve things to the client. This method tries to do this.
			thread = Mythread(self.client_socket, self.address)	   	  # creates a new thread for every user that connects. #Altough right now, it creates new threads all the time. FIX THIS!
			thread.start()
			self.threadlist.append(thread)
	def cleanthreadlist(self):
		for i in threading.enumerate():
			if not i.is_alive():
				i.join()
def main():
	print("Welcome to KTH/Hariz Bankomatic Server. This is the real time activity log screen. \nTo edit the server please login via the client. \n###########################################################")
	print("The database is now loading...")
	time.sleep(1)										# Goes to sleep for 1 second to create a more natural interaction
	myserv.inlasning()									# This method reads all the data
	print("Loading finished. Continue: ")
	time.sleep(0.2)
	print(" Currently there are: ", len(myserv.lista), "users registered. \n The average bankaccount is at:", myserv.totalcash() / myserv.antalrader, ". \n" + 
		  " MAGNITUDE of the vault cash:", myserv.storleksord(), "(" + myserv.cashvolym() + ")")
	time.sleep(1)
	print(" Server Activated and online.\n###########################################################\n")
	myserv.online()
myserv = Server()										# Creates the server (Hardcoded)
main()