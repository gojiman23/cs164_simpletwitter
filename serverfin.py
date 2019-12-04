import random
import select
import socket
import sys
import time
from socket import timeout
from thread import *
import threading
import string

#list of usernames/passwords
login_info = [('test1', 'pass1'), ('test2', 'pass2'), ('test3', 'pass3')]
#list of subscriptions
sub1 = [], sub2 = [], sub3 = []

def admin(server):
	print 'ADMIN FILLER'

def server_start(): 
	HOST = ''   # Symbolic name meaning all available interfaces
	PORT = 8888 # Arbitrary non-privileged port
	 
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
	logged_in = 0
	#conn.send('test')
	def verify(name_list, un):
		for item in name_list:
			if item[0] == un:
				return 1
	
	while(1):
		#receive/verify login credentials
		while (not logged_in):
			print 'receving'
			username = conn.recv(1024)
			pw = conn.recv(1024)
			print 'received'
			if verify(login_info, username) = 1:
				if(login_info[username] == pw):
					logged_in = 1
					print 'Log in successful'
					reply = 'Login verified'
					conn.send(reply)
			else:
				reply = 'Verification failed. Try again'
				conn.send(reply)
		
		logged_out = 0	
		#show user unread messages	
		msg = "You have 6 unread  messages"
		conn.send(msg)

		#menu handler
		while not logged_out:
			#receive client's choice
			choice = conn.recv(1024)

			if choice == 'view':
				#TODO: view messages option

			elif choice == 'edit':
				edit_handler(conn)

			elif choice == 'post':
				msg_handler(conn)

			elif choice == 'logout':
				print 'Bye!'
				# msg = 'Logout successful.'
				# conn.send(msg)		
				logged_out = 1	

def edit_handler(conn):
	d = conn.recv(1024)
	if d == 'add':
		name_good = 0
		name = s.recv(1024)
		if verify(login_info, name):
			name_good = 1
			conn.send(name_good)
			if username == 'test1':
				sub1.append(name)
			if username == 'test2':
				sub1.append(name)
			if username == 'test3':
				sub1.append(name)
		else:
			conn.send(name_good)
	elif d == 'delete':
		def removesub(sub):
			name = conn.recv(1024)
			if verify(sub, name):
				sub.remove(name)
			conn.send(sub)			
		if username == 'test1':
			conn.send(str(sub1))
			removesub(sub1)
		elif username == 'test2':
			conn.send(str(sub2))
			removesub(sub2)
		elif username == 'test3':
			conn.send(str(sub3))	
			removesub(sub3)

def msg_handler(conn):
	msg_good = 0
	while not msg_good:
		msg = conn.recv(1024)
		if len(msg) > 140:
			reply = 'Error: Message exceeds the character limit. Please try again or cancel'
		else:
			reply = 'Would you like to add any hashtags?'
			msg_good = 1
		conn.send(reply)
	hashtags = conn.recv(1024)

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