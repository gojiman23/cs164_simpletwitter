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

HOST = ''  
PORT = 9552 

#list of all users
all_users = []
#list of current users
curr_users = []
#list of all hashtags
all_hashtags = defaultdict(list)
#list of messages that need to be sent out
to_send = defaultdict(list)

msgCount = 0
counter = 0
#user class
class User:
	def __init__(self, user, passw):
		self.un = user
		self.pw = passw
		self.subList = []
		self.msgList = defaultdict(list)
		self.hashList = defaultdict(list)
		self.numUnread = 0
		self.sock = socket.socket()
	
#hard-coding users
user1 = User("test1", "test1")
user2 = User("test2", "test2")
user3 = User("test3", "test3")
user4 = User("test", "test")

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
def verify_pw(user, passw):
	for item in all_users:
		if item.un == user:
			if item.pw == passw:
				return item
	return -1

def admin(server):
	print 'ADMIN COMMANDS:'
	print '1. messagecount'
	print '2. usercount'
	print '3. new user'
	print 'Enter the above commands at any time. \n'
	
	while (1):
		command = raw_input()
		
		if command == 'messagecount':
			print 'Total messages since start of server: ' + str(msgCount) + '\n'
		elif command == 'usercount':
			print 'Current number of users: ' + str(len(curr_users)) + '\n'
		elif command == 'new user':
			#hard-coded for now
			user = raw_input('Enter the username for this user: ')
			passw = raw_input('Enter the password for this user: ')
			user5 = User(user, passw)
			all_users.append(user5)
			print 'User ' + user + ' created.\n'
		else:
			print 'Invalid choice.'
	

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
	
def send_new_messages(conn):
	global to_send
	d = conn.recv(1024)
	for user in curr_users:
		if to_send[user.un]:
			temp = str(to_send[user.un]).replace('[\'', '')
			temp = temp.replace('\']', '')
			user.sock.send(temp)
			#user.sock.send('0')
			user.sock.recv(1024)
	
	to_send = defaultdict(list)
	
def newClient(conn, addr):
	global msgCount
	while (1):
		logged_in = False
		logged_out = False
		
		#receive/verify login credentials
		while (not logged_in):
			username = conn.recv(4096)
			
			pw = conn.recv(4096)
			if verify_un(username) != -1 and verify_pw(username, pw) != -1:
				conn.send('1')
				logged_in = True
			else:
				conn.send('0')
		
		#set current user
		for item in all_users:
			if item.un == username:
				curr = item
				break
				
		#for message notification purposes
		curr.sock = conn
		
		curr_users.append(curr)
		print 'New login! Current users: '
		for item in curr_users:
			print item.un
		print
		
		ready = conn.recv(4096)
		#show user unread messages	
		msg = 'Welcome to Twitter.\nYou have ' + str(curr.numUnread) + ' unread messages.'
		conn.send(msg)
		
		#menu handler
		while not logged_out:
			choice = conn.recv(4096)

			if choice == 'view':
				view_handler(conn, curr)		
			elif choice == 'edit':
				edit_handler(conn, curr)
			elif choice == 'post':
				msgCount += msg_handler(conn, curr)				
			elif choice == 'hashtag':
				hash_handler(conn, curr)
			elif choice == 'logout':
				print curr.un + ' has logged out.\n'		
				logged_out = True
				
				#reset curr
				curr.msgList = defaultdict(list)
				curr.hashList = defaultdict(list)
				curr.numUnread = 0
				curr_users.remove(curr)	
				#~ 
			#~ send_new_messages(conn)

def view_handler(conn, curr):
	newList = ''
	#receive all/one choice
	d = conn.recv(4096)	
	if d == 'all':
		for item in curr.subList:
			if newList == '':
				newList = newList + item + ': ' + str(curr.msgList[item])
			else:
				newList = newList + ', ' + item + ': ' + str(curr.msgList[item])
		conn.send(newList)
		
	if d == 'one':
		for item in curr.subList:
			newList += item
			newList += ', '
		conn.send(newList)
		choice = conn.recv(4096)
		conn.send(str(curr.msgList[choice]))
	
	#send_new_messages(conn)	

def edit_handler(conn, curr):
	global counter
	newname = ''
	#receive editing choice
	d = conn.recv(4096)
	
	if d == 'add':
		#receive name of person they want to subscribe to
		name = conn.recv(4096)
		if name == curr.un:
			conn.send('suberr')
		elif verify_un(name) != -1:
			newname = name
			curr.subList.append(name)
			newsubs = ''
			for item in curr.subList:
				newsubs += item
				newsubs += ', '
			conn.send(newsubs)
		#~ else:
			#~ #TODO: fix hash sub
			#~ if name[0:4] == 'HASH:':
				#~ curr.hashList.append(name[6:])
				#~ conn.send(curr.hashList)
			#~ else:
				#~ conn.send('0')
				
	elif d == 'delete':
		#removes a subscription from the given list
		conn.send(str(curr.subList))
		name = conn.recv(4096)
		if verify_un(name) != -1:
			curr.subList.remove(verify_un(name).un)
		conn.send(str(curr.subList))

	#send_new_messages(conn)

def msg_handler(conn, curr):
	msg_good = 0
	
	while not msg_good:
		msg = conn.recv(4096)
		if(msg) == 'cancel':
			send_new_messages(conn)
			return 0
		elif len(msg) > 140:
			reply = 'Error: Message exceeds the character limit. Please try again or cancel'
		else:	
			reply = 'Please enter any hashtags (separate with ' ', hit enter if none): '
			msg_good = 1
		conn.send(reply)
		
	#TODO: add handler for multiple hashtags
	reply = conn.recv(4096)
	hashtags = [x.strip() for x in reply.split(' ') if x != ""]
	
	#adds message to list of subscribers
	for user in all_users:
		#avoids running for duplicates
		if user.un != curr.un:
			for name in user.subList:
				#if user that posted in sub list of another logged in user
				if curr.un == name:
					#send msg immedidately if subscriber is logged in
					#~ if user in curr_users:
						#~ to_send[user.un].append(curr.un + ": " + msg + ', ')
					#~ else:
						user.numUnread += 1
						user.msgList[curr.un].append(msg)
					
			#~ #TODO: add to hash list - EC
			#~ for hasht in item.hashList:
				#~ if hashtag == hasht:
					#~ item.msgList[hasht].append(msg)
					#~ item.numUnread += 1
	
	#add hashtag to main list
	for tag in hashtags:
		all_hashtags[tag].append(msg)
	
	#send_new_messages(conn)	
	
	return 1
	
def hash_handler(conn, curr):
	d = conn.recv(4096)
	
	if d != 'cancel':
		
		#only send up to 10 hashtags
		if len(all_hashtags[d]) <= 10:
			conn.send(str(all_hashtags[d]))
		else:
			max = len(all_hashtags[d])
			min = max-10
			conn.send(str(all_hashtags[d][min:max]))

	#send_new_messages(conn)	

	

# MAIN
event = threading.Event()

s = server_start()
s.listen(10)
print 'Server now listening'

start_new_thread(admin, (s, ))

while 1:
	#accept new connection
	conn, clientAddr = s.accept()
			
	client_msg = conn.recvfrom(4096)
	conn.send('Server echo')
	start_new_thread(newClient, (conn, clientAddr,))
	
s.close()
