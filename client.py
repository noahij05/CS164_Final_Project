import socket
import sys
from thread import *
import getpass
import os
import time
from datetime import datetime


'''
Function Definition
'''
def receiveThread(s):
	while True:
		try:
			reply = s.recv(4096) # receive msg from server
			print reply
			# You can add operations below once you receive msg
			# from the server

		except:
			print "Connection closed"
			break
	

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''
host = ''
port = 9846
try:
	remote_ip = '10.0.0.4'  #socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

welcome = s.recv(1024)
print welcome

'''
TODO: Part-1.1, 1.2: 
Enter Username and Passwd
'''
# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden). 
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()

# Send username && passwd to server
usr = raw_input('Username: ')
pas = getpass.getpass(prompt = 'Password: ')

validation = usr + '<>' + pas

s.send(validation)

reply = s.recv(5)
if reply == 'valid':
	print 'Username and password valid'
	ss = s.recv(4096)
	'''
	Part-2: Please printout the number of unread message once a new client login
	'''
	print ss

	start_new_thread(receiveThread, (s,))
	message = ""
	while True :
		
		mess = 0
		congest = 1
		if usr == 'user1':
			while(congest):
				s.send('2')
				print 'sent 2'
				time.sleep(0.2)
				s.send('1')
				time.sleep(0.2)
				print 'sent 1'
				now = datetime.now()
				curr_time = now.strftime('%H:%M:%S')
				toSend = "hellllll00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, at time = " + curr_time
				s.send(toSend)
				time.sleep(0.2)
				print 'sent ' + toSend
				s.send('user2')
				time.sleep(0.2)
				print 'sent user2'
				mess += 1
				if mess > 100:
					congest = 0
				time.sleep(1)
				
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Send messages \n 3. Group Configuration \n 4. Offline/Unread message \n")		
		try :
			s.send(message)
			if message == str(1):
				break
				
			if message == str(2):
				while True:
					option = raw_input("Choose an option (type the number): \n 1. Private messages \n 2. Broadcast messages \n 3. Group messages \n")
					try :
						'''
						Part-2: Send option to server
						'''
						s.send(option)

						if option == str(1):
							pmsg = raw_input("Enter your private message\n")
							try :
								'''
								Part-2: Send private message
								'''
								s.send(pmsg)
							except socket.error:
								print 'Private Message Send failed'
								sys.exit()
							rcv_id = raw_input("Enter the recevier ID:\n")
							try :
								'''
								Part-2: Send private message
								'''
								s.send(rcv_id)
								break
							except socket.error:
								print 'rcv_id Send failed'
								sys.exit()
						if option == str(2):
							bmsg = raw_input("Enter your broadcast message\n")
							try :
								'''
								Part-2: Send broadcast message
								'''
								s.send(bmsg)
								break
							except socket.error:
								print 'Broadcast Message Send failed'
								sys.exit()
						if option == str(3):
							gmsg = raw_input("Enter your group message\n")
							try :
								'''
								Part-2: Send group message
								'''
								s.send(gmsg)
							except socket.error:
								print 'Group Message Send failed'
								sys.exit()
							g_id = raw_input("Enter the Group ID:\n")
							try :
								'''
								Part-2: Send group message
								'''
								s.send(g_id)
								time.sleep(1)
								break
							except socket.error:
								print 'g_id Send failed'
								sys.exit()
					except socket.error:
						print 'Message Send failed'
						sys.exit() 
					
			if message == str(3):
				option = raw_input("Do you want to: 1. Join Group 2. Quit Group: \n")
				s.send(option)
				if option == str(1):
					time.sleep(1)
					group = raw_input("Enter the Group you want to join:\n")
					try :
						'''
						Part-2: Join a particular group
						'''
						s.send(group)
						time.sleep(1)
					except socket.error:
						print 'group info sent failed'
						sys.exit()
				elif option == str(2):
					time.sleep(1)
					group = raw_input("Enter the Group you want to quit:\n")
					try :
						'''
						Part-2: Quit a particular group
						'''
						s.send(group)
						time.sleep(1)
					except socket.error:
						print 'group info sent failed'
						sys.exit()
				else:
					print 'Option not valid'
			
			if message == str(4):
				option = raw_input("Do you want to 1. Read all offline/unread messages 2. Only read messages from a particular group: \n")
				s.send(option)
				if option == str(1):
					print "All offline/unread messages:"
					time.sleep(1)

				elif option == str(2):
					group = raw_input("Which group messages would you like to view?\n")
					s.send(group)
					time.sleep(1)
				else:
					print 'Option not valid'
								
		except socket.error:
			print 'Send failed'
			sys.exit()
		
else:
	print 'Invalid username or passwword'


'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side. 

reply = s.recv(5)
if reply == 'valid': # TODO: use the correct string to replace xxx here!

	# Start the receiving thread
	start_new_thread(receiveThread ,(s,))

	message = ""
	while True :

		# TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Change Password \n 3. Post Message \n")
		
		try :
			# TODO: Send the selected option to the server
			# HINT: use sendto()/sendall()
			if message == str(1):
				print 'Logout'
				# TODO: add logout operation
				s.send('1')
				s.close()
				sys.exit()

			if message == str(2):
				print('Change Password, Please enter old Password')
				s.send('2')
				oldpas = getpass.getpass(prompt = 'Old Password: ')
				if oldpas == pas:
					newpas = getpass.getpass(prompt = 'New Password: ')
					s.send(newpas)
					print 'Updated Password!'
				else:
					print 'Old Password did not match!'

			if message == str(3):
				print 'Post a message'
				s.send('3')
				msg = raw_input('Type what you want to send: ')
				s.send(msg)
				
		except socket.error:
			print 'Send failed'
			sys.exit()
else:
	print 'Invalid username or passwword'
'''
s.close()

