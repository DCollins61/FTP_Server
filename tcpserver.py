#############
# python tcpserver.py
# usage: python tcpserver.py <Port number>
#############

import socket
import sys
import os

BUFFER_SIZE = 512

if (len(sys.argv) < 2):
    print('usage: python udpserver.py <Port number>')
    sys.exit()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', int(sys.argv[1]))
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(BUFFER_SIZE)
            print >>sys.stderr, 'received %s bytes: %s' % (len(data), data)
            #Retrieve filename
            if (data[:2] == "*1"):
                rawData = data[3:]

                print >> sys.stderr, 'Client %s requests a file name [%s]' % (client_address[0], rawData)

                cwd = os.getcwd()
                path = cwd + '/%s' % rawData

                yesNoStr = '[*1:%s:' % rawData

                if os.path.exists(path):
                    data = yesNoStr + 'yes]'
                else:
                    data = yesNoStr + 'no]'
                
                connection.send(data)
            #Copy file
            elif (data[:2] == "*2"):
                fileIn = open(data[3:], "r")           

                data = "empty string"
                while (data != ''):
                    data = fileIn.read(BUFFER_SIZE)
                    connection.send(data)
                fileIn.close()
                break
            #Exit
            elif (data[:1] == "0"):
                data = 0
                connection.send(data)

            break
        
            
    finally:
        # Clean up the connection
        connection.close()
