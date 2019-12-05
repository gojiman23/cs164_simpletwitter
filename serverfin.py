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
#list of all hashtags
all_hashtags = defaultdict(list)

msgCount = 0

#user class
class User:
	un = ''
	pw = ''
	subList = []
	msgList = defaultdict(list)
	hashList = defaultdict(list)
	numUnread = 0
	msg_rcvd = 0					#bit to store if new message received while logged in
	to_send = "New message from "		#holder to send out to a logged in user
	
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
	print 'ADMIN COMMANDS:'
	print '1. messagecount'
	print '2. usercount'
	print '3. new user'
	
	command = raw_input('Enter above commands at any time. \n')
	
	if command == 'messagecount':
		print 'Total messages since start of server: ' + str(msgCount)
	elif command == 'usercount':
		print len(curr_users)
	elif command == 'new user':
		#hard-coded for now
		user5 = User()
		user5.un = raw_input('Enter the username for this user: ')
		user5.un = raw_input('Enter the password for this user: ')
		all_users.append(user5)
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
			#send out message to logged in subscriber from previous iteration
			if curr.msg_rcvd == 0:
				conn.send('Filler')
			else:
				conn.send(curr.to_send)
				#reset
				curr.msg_rcvd = 0
				curr.to_send = 'New message from '


			#receive client's choice
			choice = conn.recv(1024)

			if choice == 'view':
				view_handler(conn, curr)
				
			elif choice == 'edit':
				edit_handler(conn, curr)

			elif choice == 'post':
				msg_handler(conn, curr)
				
			elif choice == 'hashtag':
				hash_handler(conn, curr)

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

def view_handler(conn, curr):
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

def edit_handler(conn, curr):
	#receive editing choice
	d = conn.recv(1024)
	if d == 'add':
		#receive name of person they want to subscribe to
		name = conn.recv(1024)
		if name = curr.un:
			print 'You cannot subscribe to yourself.'
		if verify_un(name) != -1:
			curr.subList.append(verify_un(name))
			newsubs = ''
			for item in curr.subList:
				newsubs += item.un
				newsubs += ', '
			conn.send(newsubs)
		else:
			#TODO: fix hash sub
			if name[0:4] == 'HASH:':
				curr.hashList.append(name[6:])
				conn.send(curr.hashList)
			else:
				conn.send('0')
	elif d == 'delete':
		#removes a subscription from the given list
		conn.send(str(curr.subList))
		name = conn.recv(1024)
		if verify_un(name) != -1:
			curr.subList.remove(verify_un(name))
		conn.send(str(curr.subList))
		
def msg_handler(conn, curr):
	msg_good = 0
	while not msg_good:
		msg = conn.recv(1024)
		if len(msg) > 140:
			reply = 'Error: Message exceeds the character limit. Please try again or cancel'
		else:
			reply = 'Please enter any hashtags (hit enter if none): '
			msg_good = 1
	conn.send(reply)
	#TODO: add handler for multiple hashtags
	hashtag = conn.recv(1024)
	#adds message to list of subscribers
	for item in all_users:
		#avoids running for duplicates
		if item.un != curr.un:
			for name in item.subList:
				#if user that posted in sub list of another logged in user
				if curr.un == name.un:
					#send msg immedidately if subscriber is logged in
					if name.un in curr_users:
						name.msg_rcvd = 1
						name.to_send = name.to_send + curr.un + ': ' + msg
					else:
						name.msgList[name.un].append(msg)
						name.numUnread += 1
					
			#TODO: add to hash list - EC, don't need
			for hasht in item.hashList:
				if hashtag == hasht:
					item.msgList[hasht].append(msg)
					item.numUnread += 1
	all_hashtags[hashtag].append(msg)
	msgCount += 1
	
def hash_handler(conn, curr):
	d = conn.recv(1024)
	
	#only send up to 10 hashtags
	if len(all_hashtags[d]) <= 10:
		conn.send(str(all_hashtags[d]))
	else:
		max = len(all_hashtags[d])
		min = max-10
		conn.send(str(all_hashtags[d][min:max]))
	

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
	#print 'Connected with ' + clientAddr[0] 
		
				
	client_msg = conn.recvfrom(1024)
	#print client_msg[0]
	conn.send('Server echo')
		
	start_new_thread(newClient, (conn, clientAddr,))
	
s.close()
