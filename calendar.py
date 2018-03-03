import threading
import time
import sys 
import utils
import hashlib #import boto3


## Main class for Calendar Application
class Calendar:

    ## @param ip_L -  list of ip addresses to connect to 
    def __init__(self, ip_L):
        # list of ip addresses to connect to
        self.ip_L = ip_L 
        print('known ips:', ip_L)

        # create log as set
        self.log = {}
        # create logical clock and init to 0
        self.clock = 0
        # create process id as sha256 hash of system time       
        self.pid_S = hashlib.sha256(str(time.time()).encode()).hexdigest()
        # create list of known processes and and self
        self.processes_L = [self.pid_S] 
        # create sqs object 
#        new_sqs = boto3.resource('sqs', 'us-east-2')

    ## turn start day/time and end day/time to valid log entry 
    ## @param s_day - starting day of entry
    ## @param s_time - starting time of entry
    ## @param e_day - ending day of entry
    ## @param e_time - ending time of entry
    def create_entry(self, p_L, s_day, s_time, e_day, e_time):
        # incriment clock every time entry is created
        self.clock += 1

        # initialize start and end as the number 0
        start = 0
        end = 0

        # create id for entry as this process's pid with 
        # the current local clock time concatonated on the end
        entry_id = self.pid_S + str(self.clock)
        
        # convert day part of start and end
        start += utils.convert_day(s_day)
        end += utils.convert_day(e_day)

        # convert time part of start and end
        start += utils.convert_time(s_time)
        end += utils.convert_time(e_time)

        return [entry_id, p_L, str(start).zfill(3), str(end).zfill(3)]

    def add_to_log(self, entry):
        self.log[entry[0]] = entry[1:]
    
    def demo_cal(self):
        entry = cal.create_entry(cal.processes_L, 'Tuesday', '22:00', 'Thursday', '6:00')
        cal.add_to_log(entry)

        entry = cal.create_entry(cal.processes_L, 'Saturday', '7:00', 'Sunday', '6:30')
        cal.add_to_log(entry)

        entry = cal.create_entry(cal.processes_L, 'Saturday', '7:00', 'Saturday', '16:30')
        cal.add_to_log(entry)

        entry = cal.create_entry(cal.processes_L, 'Monday', '0:30', 'Monday', '16:00')
        cal.add_to_log(entry)

       
        for event in cal.log.keys():
            # recreate calendar entry from dictionary
            entry = [event] 
            entry.extend(cal.log[event])
            # print that entry
            utils.print_entry(entry)

if __name__ == '__main__':
        # create new calendar passing all arguments after self
        cal = Calendar(sys.argv[1:])

        cal.demo_cal() 
