import random
import select
import socket   #for sockets
import sys  #for exit
import time
from socket import timeout

def login(s):
	logged_in = 0
	while not logged_in:	
			#data = s.recv(1024)
			#print data
			username = raw_input('Enter username : ')
			password = raw_input('Enter password : ')
			
			s.send(username)
			s.send(password)
			print 'sent'
			reply = s.recv(1024)
				
				
			print 'Server reply : ' + reply
			if(reply == 'Login verified'):
				logged_in = 1

def edit_handler(s):
	msg = raw_input('Would you like to add or delete a subscription? (add/delete/cancel)')
	s.send(msg)
	
	if msg == 'add':
		name = raw_input('Who would you like to subscribe to?')
		s.send(name)
		msg = s.recv(1024)
		if msg == 0:
			print 'Invalid name.'
		else:
			print 'You are now subscribed to ' + name
	elif msg == 'delete':
		subscribed = s.recv(1024)
		print 'Subscribers to choose from: ' + subscribed
		name = raw_input('Who would you like to unsubscribe from?')
		s.send(name)
		newList = s.recv(1024)
		print 'Updated list: ' + str(newList)
	elif msg == 'cancel':
		print 'Going back'

def msg_handler(s):
	msg_good = 0
	while not msg_good:
		msg = raw_input('Enter your message (max 140 characters)')
		if msg == 'cancel':
			print 'Going back'
			msg_good = 1
		else:
			s.send(msg)
			reply = s.recv(1024)
			if reply[0] == 'E':
				print reply
			else:
				msg = raw_input(reply)
				msg_good = 1
				s.send(msg)
						
# MAIN 
host = ''
port = 8888

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

err = s.connect_ex((host, port))
if err > 0:
	print 'Error: unable to connect'
	sys.exit()
print 'Socket connected'

while(1):
	#login before performing other code
	login(s)

	#accept notification of unread messages
	messages = s.recv(1024)
	print(messages)

	#deals with menu/choices
	logged_out = 0
	while(not logged_out):
		# msg = 'logged in'
		# s.sendto(msg, (host, port))

		print 'Menu: (type option to pick) \n See Offline Messages (view) \n Edit Subscriptions (edit) \n Post a message (post) \n Hashtag Search (hashtag) \n Logout (logout)'

		choice = raw_input()
		#s.sendto(choice, (host, port))
		s.send(choice)
		if choice == 'view':
			print 'TODO'
		elif choice == 'edit':
			edit_handler(s)
		elif choice == 'post':
			msg_handler(s)
		elif choice == 'logout':
			print ('Returning to login page.')
			logged_out = 1

	
