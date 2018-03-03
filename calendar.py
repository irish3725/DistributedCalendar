import threading
import time
import sys 
import utils
import hashlib #import boto3


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
    ## @param entry_id - id of entry to be deleted
    def remove_from_log(self, entry_id):
        self.inc_clock()
        del self.log[entry_id]

    ## turn start day/time and end day/time to valid log entry 
    ## @param s_day - starting day of entry
    ## @param s_time - starting time of entry
    ## @param e_day - ending day of entry
    ## @param e_time - ending time of entry
    def create_entry(self, p_L, s_day, s_time, e_day, e_time):
        # incriment clock every time entry is created
        self.inc_clock()

        # initialize start and end as the number 0
        start = 0
        end = 0

        # create id for entry 
        # id is sha256 hash of current processor time with pid and clock time concat on end
        entry_id = hashlib.sha256(str(time.time()).encode()).hexdigest() + str(self.pid) + str(self.clock)
        
        # convert day part of start and end
        start += utils.convert_day(s_day)
        end += utils.convert_day(e_day)
# convert time part of start and end
        start += utils.convert_time(s_time)
        end += utils.convert_time(e_time)

        return [entry_id, p_L, str(start).zfill(3), str(end).zfill(3)]

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
        self.log[entry[0]] = entry[1:]

    ## prints contents of log
    def print_log(self):
        for event in cal.log.keys():
            # recreate calendar entry from dictionary
            entry = [event] 
            entry.extend(cal.log[event])
            # print that entry
            utils.print_entry(entry)

    ## runs simple demo of calendar
    def demo_cal(self):
        entry = cal.create_entry(self.processes_L, 'Tuesday', '22:00', 'Thursday', '6:00')
        cal.add_to_log(entry)

        entry = cal.create_entry(self.processes_L, 'Saturday', '7:00', 'Sunday', '6:30')
        cal.add_to_log(entry)
        eid = entry[0]

        entry = cal.create_entry(self.processes_L, 'Saturday', '7:00', 'Saturday', '16:30')
        cal.add_to_log(entry)

        entry = cal.create_entry(self.processes_L, 'Monday', '0:30', 'Monday', '16:00')
        cal.add_to_log(entry)

        # print log
#        print('log before remove:')
#        self.print_log()
        # remove from log and print again
#        self.remove_from_log(eid)
#        print('log after remove:')
#        self.print_log()

        local_T = [[5,6,8,1], [4,6,0,0], [0,0,8,1], [0,0,0,1]]
        received_T = [[4,0,0,0], [4,9,6,4], [0,0,6,1], [0,0,6,4]]

        # print matrix
        self.T = utils.update_T(local_T, received_T, self.pid)
        
        self.get_req_log(0)
        self.get_req_log(3)

if __name__ == '__main__':
        # create new calendar passing all arguments after self
        cal = Calendar()

        cal.demo_cal() 
