import random
import select
import socket   #for sockets
import sys  #for exit
import time
from socket import timeout
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;

packetStatus = 0
logged_in = 0

while(1):
# testVariable = 0
	while(not logged_in):
		username = raw_input('Enter username : ')
		password = raw_input('Enter password : ')
		
		try :
			#Set the whole string
			s.sendto(username, (host, port))
			s.sendto(password, (host, port))
			
			#start the timer for timeout
			#s.settimeout(10)
			
			try:
				# receive data from client (data, addr)
				d = s.recvfrom(1024)
				reply = d[0]
				addr = d[1]
			
			except socket.timeout:
				
				s.sendto(username, (host, port))
				s.sendto(password, (host, port))
				
				d = s.recvfrom(1024)
				reply = d[0]
				addr = d[1]
			
			
			print 'Server reply : ' + reply
			if(reply == 'login verified'):
				logged_in = 1
		   
			
		except socket.error, msg:
			#print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

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

