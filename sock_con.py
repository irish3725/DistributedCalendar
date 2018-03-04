
import socket

class sock_con:

    def __init__(self):
        # get hostname for listening for connection
        self.host = socket.gethostname()
        # get port for listening for new connections
        self.port = 5000
        # create new socket on port and bind
        self.sock = socket.socket()
        self.sock.bind((host, port))

    ## listen to (3) new connections
    ## @param port - port number for listening connection
    def listen(self, port=5000):
        # listen for 4 connections
        self.sock.listen(3)
   
        # if given a new port, change it 
        self.port = port
    
        # get connection and address of sender
        conn, addr = self.sock.accept()
        print('New connection from:', addr)
    
        # get message contents
        data = conn.recv(1024).decode()
        print(addr, 'says:\n', data, '\n')
    
    ## connect to host 
    ## @param addr - ip address of new host
    ## @param c_port - port of new host
    def connect(self, host, c_port=5000):
        # create new socket and connect to host on that socket
        socket = socket.socket()
        socket.connect((host, c_port))

        # send on message to that host
        message = 'I smell like beef...'
        socket.send(message.encode())

        # safely shutdown and close sockets
        socket.shutdown(socket.SHUT_RDWR)
        socket.close()

        