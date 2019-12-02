import random
import select
import socket
import sys
import time
from socket import timeout
from check import ip_checksum
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

users = []
users.append("test1")
users.append("test2")
users.append("test3")

passwords = []
passwords.append("pass1")
passwords.append("pass2")
passwords.append("pass3")

while(1):

	logged_in = 0
	while(not logged_in):
	#verify username
		d = s.recvfrom(1024)
		addr = d[1]
		if d[0] == users[0]:
			d = s.recvfrom(1024)
			addr = d[1]
			if d[0] == passwords[0]:
				print 'Login success!'
				reply = 'login verified'
				logged_in = 1
				s.sendto(reply , addr)
			else:
				reply = 'verification failed. try again'
				s.sendto(reply, addr)
		elif d[0] == users[1]:
			d = s.recvfrom(1024)
			addr = d[1]
			if d[0] == passwords[1]:
				print 'Login success!'
				reply = 'login verified'
				logged_in = 1
				s.sendto(reply , addr)
			else:
				reply = 'verification failed. try again'
				s.sendto(reply, addr)
		elif d[0] == users[2]:
			d = s.recvfrom(1024)
			addr = d[1]
			if d[0] == passwords[2]:
				print 'Login success!'
				reply = 'login verified'
				logged_in = 1
				s.sendto(reply , addr)
			else:
				reply = 'verification failed. try again'
				s.sendto(reply, addr)		
			
		else:
			#catch extra password
			d = s.recvfrom(1024)
			reply = 'verification failed. try again'
			s.sendto(reply, addr)
				

	#show user unread messages	
	msg = "You have 6 unread  messages"
	s.sendto(msg, addr)

	menu = 'Menu: (type option to pick) \n See Offline Messages \n Edit Subscriptions \n Post a message \n Hashtag Search \n Logout'
	s.sendto(menu, addr)
	
	d = s.recvfrom(1024)
	choice = d[0]
	addr = d[1]
	
	if(choice == 'logout'):
		print 'Bye!'
		msg = 'Logout successful.'
		s.sendto(msg, addr)
		continue
	
#s.close()

