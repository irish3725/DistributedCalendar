import threading
import time
import sys
#import boto3


## Main class for Calendar Application
class Calendar:

    ## @param ip_L -  list of ip addresses to connect to 
    def __init__(self, ip_L):
        # list of ip addresses to connect to
        self.ip_L = ip_L 
        print('known ips:', ip_L)
#        self.log = Log.Log()
        # initialize nodes_D with self, localhost, port 5000
#        self.nodes_D = {}
        # add thread to list with localhost ip as name and start new_connection
        self.thread_L = [] 
       
        # create sqs object 
#        new_sqs = boto3.resource('sqs', 'us-east-2')

    def print_stuff(self, stuff):
        for i in range(10000000000):
            print(stuff, i)

if __name__ == '__main__':
    # create new calendar passing all arguments after self
    cal = Calendar(sys.argv[1:])
    # list of thread
    threads_L = []
    # stuff to pass print_stuff
    stuff1 ='my name is talk1' 
    stuff2 ='my name is talk2' 
    # start threads and call stuff on them
    threads_L.append(threading.Thread(name='talk1', target=cal.print_stuff, args=(stuff1,)))
    threads_L.append(threading.Thread(name='talk2', target=cal.print_stuff, args=(stuff2,)))
    # start thread
    for thread in threads_L:
        print('startinging thread:', thread.name)
        thread.start()

    for thread in threads_L:
        print('joining thread:', thread.name)
        thread.join()

