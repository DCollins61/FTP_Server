###############
# python tcpclient.py 
# usage: python tcpclient.py <IP address> <Port number>
##############

import socket
import sys
import os

BUFFER_SIZE = 512

menu = """
====Please enter the menu====
1.Request a file name (Usage: *1:filename)
2.Download a file (Usage: *2:filename)
0.Exit (Usage: 0)
"""    	 
    

if (len(sys.argv) < 3): 
    print('usage: python udpclient.py <IP address> <Port number>')
    sys.exit()
# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (sys.argv[1], int(sys.argv[2]))
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address) 

print menu 
userinput = raw_input("Please enter: ")
message = userinput

try:
    rawFile = message[3:]
    if (message[:2] == "*1"):
        # Send data
        sent = sock.send(message)

        # Receive response
        data = sock.recv(BUFFER_SIZE)
        print >>sys.stderr, 'Received: %s' % data

    elif (message[:2] == "*2"):
        # Send data
        sent = sock.send(message)

        data = " "

        cwd = os.getcwd()
        # Creating a new file to hold the copied data
        while True:
            path = cwd + '/%s' % rawFile
            if (os.path.exists(path)):
                rawFile = rawFile.replace(".txt", "2.txt")
            else:
                break
        outFile = open(rawFile, "a")
        
        while (data != ''):
        # Receive response
            data = sock.recv(BUFFER_SIZE)
            outFile.write(data)

        outFile.close()
        print >> sys.stderr, 'Successfully copied file!'

    elif (message[:1] == "0"):
        print >> sys.stderr, 'Exiting...'
        
    else:
        print >> sys.stderr, '%s is not a valid command!' % (message)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
