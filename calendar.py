import socket
import threading
import sys

## Main class for Calendar Application
class Calendar:
 
    def __init__(self):
#        self.log = Log.Log()
        # initialize nodes_D with self, localhost, port 5000
        self.nodes_D = {'127.0.0.1' : 5000}
        # add thread to list with localhost ip as name and start new_connection
        thread_L = [threading.Thread(name='127.0.0.1', target=self.new_connection('127.0.0.1'))] 

    ## @param name - name of new connection 
    def new_connection(self, name):
       
        # hose is inputted name 
        host = name
        # port is dict entry at name
        port = self.nodes_D[name] 
         
        mySocket = socket.socket()
        mySocket.bind((host,port))
         
        mySocket.listen(1)
        conn, addr = mySocket.accept()
        print ("Connection from: " + str(addr))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                    break
            print ("from connected  user: " + str(data))
             
            data = str(data).upper()
            print ("sending: " + str(data))
            conn.send(data.encode())
                 
        conn.close()
         
if __name__ == '__main__':
    cal = Calendar()
