import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
HOST = ''	# Symbolic name meaning all available interfaces
PORT = 9846	# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

'''
Bind socket to local host and port
'''
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'


clients = []

userpass = [["user1", "passwd1"], ["user2", "passwd2"], ["user3", "passwd3"]]
messages = [[],[],[]]
subscriptions = [[],[],[]] # Store the group info
groups = ["group1", "group2", "group3"]


def clientthread(conn):
	global clients
	global count
	conn.send("Welcome to CS164Book! Please log in")
	uppair = conn.recv(1024)
	uppair = stringToTuple(uppair)
	if uppair in userpass:
		user = userpass.index(uppair)
		try:
			conn.sendall('valid')
		except socket.error:
			print 'Send Failed!'
			sys.exit()
		
		
		unreadnum = 'You have ' +  str(len(messages[user])) + ' unread messages.'
		conn.sendall(unreadnum)

		while True:
			try :
				option = conn.recv(1024)
			except:
				break
			if option == str(1):
				# Logout that you implemented in Part-1
				break;
			elif option == str(2):
				message = conn.recv(1024)
				if message == str(1):
					'''
					Part-2: Send private message
					'''
					toSend = conn.recv(4096)
					toSend = 'Message from ' + uppair[0] + ': ' + toSend
					whomSend = conn.recv(1024)
					for x in range(len(userpass)):
						if whomSend in userpass[x]:
							messages[x].append(toSend)
					
				if message == str(2):
					'''
					Part-2: Send broadcast message
					'''
					toSend = conn.recv(1024)
					toSend = "Message from " + uppair[0] + ": " + toSend
					for c in clients:
						if c == conn:
							continue
						c.sendall(toSend)
							
				if message == str(3):
					'''
					Part-2: Send group message
					'''
					toSend = conn.recv(1024)
					whomSend = conn.recv(1024)
					toSend = whomSend + ' message from ' + uppair[0]  +  ': ' + toSend
					if whomSend in subscriptions[user]:
						for x in range(len(subscriptions)):
							if whomSend in subscriptions[x] and x is not user:
								messages[x].append(toSend)
					else:
						conn.send('You are not a member of ' + whomSend + ' please request to join first!')
			elif option == str(3):
				'''
				Part-2: Join/Quit group
				'''
				message = conn.recv(1024)
				if message == str(1):
					toSend = 'Groups to join:\n'
					for x in groups:
						toSend = toSend + x + '\n'
					conn.sendall(toSend)
					toJoin = conn.recv(1024)
					if toJoin in subscriptions[user]:
						conn.sendall('Already in this group!')
					else:
						if toJoin in groups:
							subscriptions[user].append(toJoin)
							conn.sendall('Successfully joined ' + toJoin)
						else:
							conn.sendall('Group does not exist!')
				if message == str(2):
					toSend = 'Groups to quit:\n'
					for x in subscriptions[user]:
						toSend = toSend + x + '\n'
					conn.sendall(toSend)
					toQuit = conn.recv(1024)
					if toQuit in subscriptions[user]:
						subscriptions[user].remove(toQuit)
						conn.sendall('Successfully quit ' + toQuit)
					else:
						conn.sendall('You are not subscribed to this group')
					
			elif option == str(4):
				'''
				Part-2: Read offline message
				'''
				message = conn.recv(1024)
				if message == str(1):
					toSend = ''
					for msg in messages[user]:
						toSend = toSend + msg + '\n'
					conn.send(toSend)
					messages[user] = []
				if message == str(2):
					groupToRead = conn.recv(1024)
					toSend = 'Messages from ' + groupToRead + ':\n' 
					for msg in messages[user]:
						ok = msg.split(' ', -1)
						print ok[0]
						if groupToRead == ok[0]:
							toSend = toSend + msg + '\n'
							messages[user].remove(msg)
					conn.sendall(toSend)
					
							


			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)
	else:
		try :
			conn.sendall('nalid')
		except socket.error:
			print 'nalid Send failed'
	print 'Logged out'
	conn.close()
	if conn in clients:
		clients.remove(conn)

'''
userpass = [['njime006', 'bruh'], ['user1', 'foo']]
messages = [[],[],[]]
count = 0


Function for handling connections. This will be used to create threads

def clientThread(conn):
	#global clients
	global count
	# Tips: Sending message to connected client
	conn.send('Welcome to the server. Type your username and password') #send only takes string
	rcv_msg = conn.recv(1024)
	rcv_msg = stringToTuple(rcv_msg)
	if rcv_msg in userpass:
		user = userpass.index(rcv_msg)
		
		try :
			conn.sendall('valid')
		except socket.error:
			print 'Send failed'
			sys.exit()
			
		# Tips: Infinite loop so that function do not terminate and thread do not end.
		while True:
			try :
				option = conn.recv(1024)
			except:
				break
			if option == str(1):
				print(rcv_msg[0]),
				break
				# TODO: Part-1: Add the logout processing here

			elif option == str(2):
				newpass = conn.recv(1024)
				userpass[user].remove(rcv_msg[1])
				userpass[user].append(newpass)
				#print userpass[user]
				  
	
			elif option == str(3):
				print 'Post a message'
				msg = conn.recv(1024)
				print 'Message to be sent to everyone by ' + rcv_msg[0] + ': ' + msg
				for conn in clients:			
					conn.sendall(msg)
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)
	else:
		try :
			conn.sendall('nalid')
		except socket.error:
			print 'nalid Send failed'
	print 'Logged out'
	conn.close()
	if conn in clients:
		clients.remove(conn)
'''
def receiveClients(s):
	global clients
	while 1:
		# Tips: Wait to accept a new connection (client) - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		# Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientthread ,(conn,))

start_new_thread(receiveClients ,(s,))

'''
main thread of the server
print out the stats

while 1:
	#receiveClients(s)
	#clientThread(conn)
	message = raw_input()
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'
s.close()
'''

while 1:
	message = raw_input()
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'
	elif message == 'listgroup':
		'''
		Part-2: Implement the functionality to list all the available groups
		'''
		for x in groups:
			print x
s.close()
