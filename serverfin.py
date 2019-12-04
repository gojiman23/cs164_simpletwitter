import random
import select
import socket
import sys
import time
from socket import timeout
from thread import *
import threading
import string
from collections import defaultdict

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

#list of all users
all_users = []
#list of current users
curr_users = []

#user class
class User:
	un = ''
	pw = ''
	subList = []
	msgList = defaultdict(list)
	hashList = defaultdict(list)
	numUnread = 0
	
#hard-coding users
user1 = User()
user1.un = "Bob"
user1.pw = "Bobby"

user2 = User()
user2.un = "Tom"
user2.pw = "Tommy"

user3 = User()
user3.un = "Rick"
user3.pw = "Ricky"

user4 = User()
user4.un = "test"
user4.pw = "test"

all_users.append(user1)
all_users.append(user2)
all_users.append(user3)
all_users.append(user4)

#check if username is valid
def verify_un(name):
	for item in all_users:
		if item.un == name:
			return item
	return -1
#check if password is valid		
def verify_pw(name):
	for item in all_users:
		if item.pw == name:
			return item
	return -1

def admin(server):
	print 'ADMIN FILLER'

def server_start():	 
	# Datagram (udp) socket
	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Socket created'
	except socket.error, msg :
		print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
	# Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
		 
	print 'Socket bind complete'
	
	return s
	
def newClient(conn, addr):
	while (1):
		logged_in = False
		logged_out = False
		#receive/verify login credentials
		while (not logged_in):
			username = conn.recv(1024)
			
			pw = conn.recv(1024)
			if verify_un(username) != -1 and verify_pw(pw) != -1:
				print 'Client login successful'
				conn.send('1')
				logged_in = True
			else:
				conn.send('0')
		
		#set current user
		for item in all_users:
			if item.un == username:
				curr = item
		
		curr_users.append(curr)
		print 'Current users: '
		for item in curr_users:
			print item.un
		print 'Beginning simple twitter app'
		#show user unread messages	
		msg = 'Welcome to Twitter.\nYou have ' + str(curr.numUnread) + ' unread messages'
		conn.send(msg)

		#menu handler
		while not logged_out:
			#receive client's choice
			choice = conn.recv(1024)

			if choice == 'view':
				view_handler(conn, username, curr)
				
			elif choice == 'edit':
				edit_handler(conn, username, curr)

			elif choice == 'post':
				msg_handler(conn, username, curr)

			elif choice == 'logout':
				print 'Bye!'
				# msg = 'Logout successful.'
				# conn.send(msg)		
				logged_out = True
				#reset curr
				curr.msgList = defaultdict(list)
				curr.hashList = defaultdict(list)
				curr.numUnread = 0
				curr_users.remove(curr)	

def view_handler(conn, username, curr):
	#receive all/one choice
	d = conn.recv(1024)	
	if d == 'all':
		conn.send(str(curr.msgList))
	if d == 'one':
		newList = ''
		for item in curr.subList:
			newList += item.un
			newList += ', '
		conn.send(newList)
		choice = conn.recv(1024)
		conn.send(str(curr.msgList[choice]))

def edit_handler(conn, username, curr):
	#receive editing choice
	d = conn.recv(1024)
	if d == 'add':
		#receive name of person they want to subscribe to
		name = conn.recv(1024)
		if verify_un(name) != -1:
			curr.subList.append(verify_un(name))
			newsubs = ''
			for item in curr.subList:
				newsubs += item.un
				newsubs += ', '
			conn.send(newsubs)
		else:
			conn.send('0')
	elif d == 'delete':
		#removes a subscription from the given list
		conn.send(str(curr.subList))
		name = conn.recv(1024)
		if verify_un(name) != -1:
			curr.subList.remove(verify_un(name))
		conn.send(str(curr.subList))
		
def msg_handler(conn, username, curr):
	msg_good = 0
	while not msg_good:
		msg = conn.recv(1024)
		if len(msg) > 140:
			reply = 'Error: Message exceeds the character limit. Please try again or cancel'
		else:
			reply = 'Please enter any hashtags (optional, put no if N/A): '
			msg_fin = msg	#store for later
			msg_good = 1
	conn.send(reply)
	#TODO: add handler for multiple hashtags
	hashtags = conn.recv(1024)
	if hashtags == 'no':	#only accept if hashtag entry is not 'no'
		hashtags = ''
	
	
	#adds message to list of subscribers
	for item in curr_users:
		if item.un != curr.un:
			for name in item.subList:
				if curr.un == name.un:
					name.msgList[name.un].append(msg)
					name.hashList[hashtags].append(msg)
					name.numUnread += 1


# MAIN
event = threading.Event()

s = server_start()
s.listen(10)
print 'Server now listening'

start_new_thread(admin, (s, ))

while 1:
	#accept new connection
	conn, clientAddr = s.accept()
	
	#display newly connected client
	print 'Connected with ' + clientAddr[0] 
		
				
	client_msg = conn.recvfrom(1024)
	print client_msg[0]
	conn.send('Server echo')
		
	start_new_thread(newClient, (conn, clientAddr,))
	
s.close()

#~ while(1):
	#~ d = s.recvfrom(1024)
	#~ addr = d[1]
#~ 
	#~ if d[0] == 'login':
	#~ #verify username
		#~ d = s.recvfrom(1024)
		#~ addr = d[1]
		#~ if d[0] == users[0]:
			#~ d = s.recvfrom(1024)
			#~ addr = d[1]
			#~ if d[0] == passwords[0]:
				#~ print 'Login success!'
				#~ reply = 'Login verified'
				#~ logged_in = 1
				#~ s.sendto(reply , addr)
			#~ else:
				#~ reply = 'Verification failed. Try again'
				#~ s.sendto(reply, addr)
		#~ elif d[0] == users[1]:
			#~ d = s.recvfrom(1024)
			#~ addr = d[1]
			#~ if d[0] == passwords[1]:
				#~ print 'Login success!'
				#~ reply = 'Login verified'
				#~ logged_in = 1
				#~ s.sendto(reply , addr)
			#~ else:
				#~ reply = 'Verification failed. Try again'
				#~ s.sendto(reply, addr)
		#~ elif d[0] == users[2]:
			#~ d = s.recvfrom(1024)
			#~ addr = d[1]
			#~ if d[0] == passwords[2]:
				#~ print 'Login success!'
				#~ reply = 'Login verified'
				#~ logged_in = 1
				#~ s.sendto(reply , addr)
			#~ else:
				#~ reply = 'Verification failed. Try again'
				#~ s.sendto(reply, addr)		
			#~ 
		#~ else:
			#~ #catch extra password
			#~ d = s.recvfrom(1024)
			#~ addr = d[1]
			#~ reply = 'Verification failed. Try again'
			#~ s.sendto(reply, addr) passwords[1]:
				#~ print 'Login success!'
				#~ reply = 'Login verified'
				#~ logged_in = 1
				#~ s.sendto(reply , addr)
			#~ else:
				#~ reply = 'Verification failed. Try again'
				#~ s.sendto(reply, addr)
		#~ elif d[0] == users[2]:
			#~ d = s.recvfrom(1024)
			#~ addr = d[1]
			#~ if d[0] == passwords[2]:
				#~ print 'Login success!'
				#~ reply = 'Login verified'
				#~ logged_in = 1
				#~ s.sendto(reply , addr)
			#~ else:
				#~ reply = 'Verification failed. Try again'
				#~ s.sendto(reply, addr)		
			#~ 
		#~ else:
			#~ #catch extra password
			#~ d = s.recvfrom(1024)
			#~ addr = d[1]
			#~ reply = 'Verification failed. Try again'
			#~ s.sendto(reply, addr)
			#~ 
	#~ elif d[0] == 'logged in':
		#~ #show user unread messages	
		#~ msg = "You have 6 unread  messages"
		#~ s.sendto(msg, addr)
#~ 
		#~ menu = 'Menu: (type option to pick) \n See Offline Messages(view) \n Edit Subscriptions (edit) \n Post a message \n Hashtag Search \n Logout (logout)'
		#~ s.sendto(menu, addr)
		#~ 
		#~ d = s.recvfrom(1024)
		#~ choice = d[0]
		#~ addr = d[1]
		#~ 
		#~ if(choice == 'view'):
			#~ msg = 'Would you like to see all messages or would you like to see messages from a particular subscription? (all/particular)'
			#~ s.sendto(msg, addr)
			#~ d = s.recvfrom
		#~ 
		#~ elif (choice == 'edit'):
			#~ msg = 'Would you like to add or delete a subscription? (add/delete)'
			#~ s.sendto(msg, addr)
			#~ d = s.recvfrom(1024)
			#~ addr = d[1]
			#~ if d[0] == 'add':
				#~ name = raw_input('Who would you like to subscribe to?')
				#~ if name == users[0] or name == users[1] or name == users[2]:
					#~ print 'You are now subscribed to ' + name
					#~ #TODO: append subscribed user to subscribee's persona list
					#~ 
		#~ 
		#~ elif(choice == 'logout'):
			#~ print 'Bye!'
			#~ msg = 'Logout successful.'
			#~ s.sendto(msg, addr)
			#~ continue	
