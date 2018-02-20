import socket
from random import randint
import threading
import sys

## Main class for Calendar Application
class Calendar:
 
    def __init__(self):
#        self.log = Log.Log()
        # initialize nodes_D with self, localhost, port 5000
        self.nodes_D = {}
        # add thread to list with localhost ip as name and start new_connection
        self.thread_L = [] 
        # start listening for new connections
        self.start_listen()

    ## create thread to listen for new connections
    def start_listen(self):
        print('listening on port 5000')

    ## listen for new connections
    def listen(self):
        # host is this computer
        host = socket.gethostname()
     
        # port is 5000
        port = 5000
 
        # create new socket 
        new_socket = socket.socket()
        new_socket.bind((host,port))
         
        new_socket.listen(1)
        
        conn, addr = new_socket.accept()
        print("new connection from: " + str(addr))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                    break
            print ("from connected  user: " + str(data))
             
            data = str(data).upper()
         
            
        
        conn.close()

    def connect_perm_connection(self, host, port):
        # create new socket 
        new_socket = socket.socket()
        new_socket.connect((host, port))
         
        # send other host info for this node
        message = 'we did it!!'       
        new_socket.send(message.encode())

    def listen_perm_connection(self, port):
        # host is this computer
        host = socket.gethostname()
 
        # create new socket 
        new_socket = socket.socket()
        new_socket.bind((host,port))
         
        new_socket.listen(1)
        
        conn, addr = new_socket.accept()
        print("Connection from", str(addr), 'on port', port)
        while True:
            data = conn.recv(1024).decode()
            if not data:
                    break
            print("from", str(addr), ':', str(data))
             
            data = str(data).upper()
            print("sending", str(data), 'to', str(add))
            conn.send(data.encode())
                 
        conn.close()        

    ## @param host - ip of new host
    def add_connection(self, host):
 
        # find a port to put new connection on 
        port = 5000
        while port in self.nodes_D.items():
            port = randint(5001,6000)       
 
        # add host and port to nodes_D
        self.nodes_D[host] = port
 
        # create new socket 
        new_socket = socket.socket()
        new_socket.connect((host, 5000))
         
        # send other host info for this node
        message = str(port)       
        new_socket.send(message.encode())
       
        # start perminant connection on another port
        perm_connection(port)
 
if __name__ == '__main__':
    # create new calendar
    cal = Calendar()
    
    # listen on listen_thread
    listen_thread = threading.Thread(name='listen', target=cal.listen)
    print('made it past listen_thread line')
    # append thread to our list
    cal.thread_L.append(listen_thread)
    # start thread
    listen_thread.start()

    # if arguments are given, add them to connections
    if len(sys.argv) > 1:
        for ip in sys.argv:
            if ip != 'calendar.py':
                print('Connecting to ' + ip)
                new_thread = threading.Thread(name=ip, target=cal.add_connection, args=(ip, ))
                cal.thread_L.append(new_thread)
                new_thread.start() 

    for thread in cal.thread_L:
        print('joining thread:', thread.name)
        thread.join()

