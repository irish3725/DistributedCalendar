import socket
import sys
 
def Main():

    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = '127.0.0.1'

    port = 5000
     
    mySocket = socket.socket()
    mySocket.connect((host,port))
     
    message = input(" -> ")
     
    while message != 'q':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()
         
        print ('Received from server: ' + data)
         
        message = input(" -> ")
             
    mySocket.close()
 
if __name__ == '__main__':
    Main()
