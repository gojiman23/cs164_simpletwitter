import random
import select
import socket   #for sockets
import sys  #for exit
import time
from socket import timeout

#from check import ip_checksum
 
host = '';
port = 8888;

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

#login before performing other code
logged_in = 0
while(1):
	if not logged_in:	
		
			data = s.recv(1024)
			print data
			username = raw_input('Enter username : ')
			password = raw_input('Enter password : ')
			
			s.send(username)
			s.send(password)
			print 'sent'
			d = s.recv(1024)
				
				
			print 'Server reply : ' + reply
			if(reply == 'Login verified'):
				logged_in = 1
				

	else:
	# testVariable = 0
		msg = 'logged in'
		s.sendto(msg, (host, port))
		d = s.recvfrom(1024)
		reply = d[0]
		print reply
		

		d = s.recvfrom(1024)
		reply = d[0]
		print reply

		choice = raw_input()
		s.sendto(choice, (host, port))

		d = s.recvfrom(1024)
		if (d[0] == 'Logout successful.'):
			print ('Returning to login page.')
			logged_in = 0

