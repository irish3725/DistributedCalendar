import threading

    ips_L = ['153.90.19.213', '18.222.71.71']

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

