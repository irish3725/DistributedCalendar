import threading
import time
import sys 
import hashlib 
#import boto3
# import helper files
import ui as UI 
import utils


## Main class for Calendar Application
class Calendar:

    ## @param my_id - id of this process
    def __init__(self, my_id=0):
        # create log as set
        self.log = {}
        # create logical clock and init to 0
        self.clock = 0
        # create process id as sha256 hash of system time       
        self.pid = my_id
        # create list of known processes and and self
        self.processes_L = [my_id] 
        # create T with all spots initialized to 0
        self.T = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        # create sqs object 
#        new_sqs = boto3.resource('sqs', 'us-east-2')

    ## incriments clock and correct spot in self.T
    def inc_clock(self):
        self.clock += 1
        self.T[self.pid][self.pid] = self.clock

    ## deletes entry with that entry id
    ## @param uid - id of user who created the event
    ## @param c_val - clock value of user who created the event
    def remove_from_log(self, name):
        self.inc_clock()
        for e_name in self.log.keys():
            if name.lower() == e_name.lower():
                del self.log[name]
                print('Removed', name, 'from calendar.\nHere is what the calendar looks like so far:')
                self.print_log()
                print()
                return
        print('Failed to remove', name, 'from calendar.\nHere is what the calendar looks like so far:')
        self.print_log()
        print()
        return False

    ## turn start day/time and end day/time to valid log entry 
    ## @param name - name of appointment
    ## @param day - starting day of entry
    ## @param s_time - starting time of entry
    ## @param e_time - ending day of entry
    ## @param p_L - list of processes involved
    def create_entry(self, name, day, s_time, e_time, p_L):
        # incriment clock every time entry is created
        self.inc_clock()

        # initialize start and end as the number 0
        start = 0
        end = 0

        # create id for entry 
        # id is sha256 hash of current processor time with pid and clock time concat on end
        entry_id = hashlib.sha256(str(time.time()).encode()).hexdigest() + str(self.pid) + str(self.clock).zfill(3)
        
        # convert day part of start and end
        start += utils.convert_day(day)
        end += utils.convert_day(day)
# convert time part of start and end
        start += utils.convert_time(s_time)
        end += utils.convert_time(e_time)

        return [name.lower(), entry_id, str(start).zfill(3), str(end).zfill(3), p_L]

    ## returns the log excluding entries that the receiver knows
    ## @param to_id - id of process to be receiving message
    def get_req_log(self, to_id):
        send_log = self.log
        # iterate over keys in log
        for entry in self.log.keys():
            
            creator = int(entry[64:65])
            created_at = int(entry[65:])
            # if created at time is smaller than entry in T
            if self.T[to_id][creator] < created_at:
                # delete entry
                send_log[entry] = self.log[entry]
                print('creating entry')
                print('pid of creator:', entry[64:65])
                print('clock time at creation:', entry[65:])

        print

    ## adds entry to log
    ## @param entry - entry to be entered into log
    def add_to_log(self, entry):
        if self.check_log(entry):
            self.log[entry[0]] = entry[1:]
            return True
        return False

    ## makes sure log entry does not overlap with other entries
    def check_log(self, entry):
        if not self.log.keys():
            return True
        for name in self.log.keys():
            # check to see if name is unique
            if name == entry[0]:
                print('There is already an entry in the log with this name.')
                return False
            # check to see if processes overlap
            for p in entry[4]:
                if p in self.log[name][3]:
                    # if start time of new is before end time of old
                    # and end time of new is after start time of old, they overlap
                    if self.log[name][1] < entry[3] and self.log[name][2] > entry[2]:
                        print('There is a conflict with process', p, '.\n', entry[0], 'will not be addes.')
                        return False
        return True

    ## prints contents of log
    def print_log(self, everyone=False):
        empty = True
        for event in self.log.keys():
            print(self.log[event][3])
            if everyone or self.pid in self.log[event][3]:
                empty = False
                # recreate calendar entry from dictionary
                entry = [event] 
                entry.extend(cal.log[event])
                # print that entry
                utils.print_entry(entry)
        if empty:
            print('Nothing in calendar')
        
    ## creates calendar event, adds it to log, and sends update message to everyone
    ## @param name - name of event
    ## @param day - starting day of entry
    ## @param s_time - starting time of entry
    ## @param e_time - ending time of entry
    ## @param p_L - list of processes involvedlj
    def add_event(self, name, day, s_time, e_time, p_L):
        event = self.create_entry(name, day, s_time, e_time, p_L)
        if self.add_to_log(event):
            print('Added event to calendar.\nHere is what the calendar looks like so far:')
        self.print_log()
        print()

    ## runs simple demo of calendar
    def demo_cal(self):

        entry = cal.create_entry('Event1', 'Tuesday', '2:00', '6:00', [0,1,2,] )
        cal.add_to_log(entry)
        eid = entry[0]

        entry = cal.create_entry('Event2', 'Tuesday', '12:00', '12:30', [0,2] )
        cal.add_to_log(entry)

        entry = cal.create_entry('Event3', 'Tuesday', '2:00', '6:00', [1,3] )
        cal.add_to_log(entry)
        
        entry = cal.create_entry('Event4', 'Tuesday', '2:00', '6:00', [1,3] )
        cal.add_to_log(entry)

        # print log
        print('log before remove:')
        self.print_log()
        # remove from log and print again
        self.remove_from_log('Event2')

#        local_T = [[5,6,8,1], [4,6,0,0], [0,0,8,1], [0,0,0,1]]
#        received_T = [[4,0,0,0], [4,9,6,4], [0,0,6,1], [0,0,6,4]]

        # print matrix
#        self.T = utils.update_T(local_T, received_T, self.pid)
        
#        self.get_req_log(0)
#        self.get_req_log(3)

if __name__ == '__main__':
    # create new calendar passing all arguments after self
    cal = Calendar()

    threads_L = []

    # if input arguments are given, run demo
    if len(sys.argv) > 1:
        cal.demo_cal() 
    else:
        # create ui
        ui = UI.ui(cal)
        threads_L.append(threading.Thread(name='ui', target=ui.run))
        
        # start threads
        for thread in threads_L:
            thread.start()

        # join threads
        for thread in threads_L:
            thread.join()

