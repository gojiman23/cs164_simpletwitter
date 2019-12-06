import random
import select
import socket   #for sockets
import sys  #for exit
import time
from socket import timeout

logged_out = 0

def login(s):
	while(1):
		logged_in = '0'
		while logged_in == '0':	
			username = raw_input('Enter username : ')
			s.send(username)
			password = raw_input('Enter password : ')
			s.send(password)

			reply = s.recv(1024)
			print 'login received'				
			logged_in = reply[0:1]
			if logged_in == '0':
				print "Invalid username and/or password. Please try again"
		
		print "Login success!\n"
		
		ready = 'Ready to start'
		s.send(ready)
		#~ #accept notification of unread messages
		messages = s.recv(1024)
		print messages
		
		#deals with menu/choices
		logged_out = 0
		while not logged_out:
			#catch trash or new message
			#~ possible = s.recv(1024)
			#~ print 'received'
			#~ if possible[0:2] == 'New':
				#~ print possible
			#~ elif possible[0:7]:
				#~ print possible
			#~ else:
				#~ print 'skipped'
			print '\nMenu: (type option to pick) \n See Offline Messages (view) \n Edit Subscriptions (edit) \n Post a message (post) \n Hashtag Search (hashtag) \n Logout (logout)'

			choice = raw_input()
			#s.sendto(choice, (host, port))
			s.send(choice)
			if choice == 'view':
				view_handler(s)
			elif choice == 'edit':
				edit_handler(s)
			elif choice == 'post':
				msg_handler(s)
			elif choice == 'hashtag':
				hash_handler(s)
			elif choice == 'logout':
				print ('Returning to login page.')
				logged_out = 1

def view_handler(s):
	msg = raw_input('Would you like to see all of your unread messages or messages from one subscription? (all/one/cancel): ')
	s.send(msg)	#send user's choice
	if msg != 'cancel':
		if msg == 'all':
			newlist = s.recv(1024)	#wait for message list
			print 'New messages: ' + newlist
		elif msg == 'one':
			newlist = s.recv(1024)	#wait for message list
			print 'Subscriptions to choose from: ' + newlist
			msg = raw_input('Which subscription would you like to choose?: ')
			s.send(msg)
			newlist = s.recv(1024)
			print 'Messages from ' + msg + ': ' + newlist
	else:
		print 'Going back'	
	
	
def edit_handler(s):
	msg = raw_input('Would you like to add or delete a subscription? (add/delete/cancel): ')
	s.send(msg)
	
	if msg == 'add':
		name = raw_input('Who would you like to subscribe to?: ')
		s.send(name)
		msg = s.recv(1024)
		if msg == 'cancel':
			print 'Going back'
		elif msg == 'suberr':
			print 'You cannot subscribe to yourself.'
		elif msg == '0':
			print 'Invalid name.'
		else:
			print 'New subscription list: ' + msg
	elif msg == 'delete':
		subscribed = s.recv(1024)
		print 'Subscribers to choose from: ' + str(subscribed)
		name = raw_input('Who would you like to unsubscribe from?: ')
		s.send(name)
		newList = s.recv(1024)
		print 'Updated list: ' + str(newList)
	elif msg == 'cancel':
		print 'Going back'

def msg_handler(s):
	msg_good = 0
	while not msg_good:
		msg = raw_input('Enter your message (max 140 characters): ')
		if msg == 'cancel':
			print 'Going back'
			msg_good = 1
		else:
			s.send(msg)
			reply = s.recv(1024)
			#prints error message if post too long
			if reply[0] == 'E':
				print reply
			#takes in hashtags
			else:
				hashtag = raw_input(reply)	
				msg_good = 1
				s.send(hashtag)
	
def hash_handler(s):
	msg = raw_input('What hashtag would you like to search up?: ')
	if msg == 'cancel':
		print 'Going back'
	else:
		s.send(msg)
		newlist = s.recv(1024)
		print 'Messages under hashtag ' + msg + ': ' + newlist
	
						
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

s.send('Client connecting')
d = s.recvfrom(1024)
print d[0]

while(1):
	#login before performing other code
	login(s)
