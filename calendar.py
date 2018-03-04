import threading
import time
import sys 
import hashlib 
from collections import Counter 
#import boto3

# import helper files
import ui as UI 
import utils


## Main class for Calendar Application
class Calendar:

    ## @param my_id - id of this process
    def __init__(self, my_id=0, new_session=True):
        # create calendar as dict
        self.calendar = [] 
        # create log as dict
        self.log = {}
        # create logical clock and init to 0
        self.clock = 0
        ## if not a new session, load from file
        if not new_session:
            print('Loading calendar from last session')
            self.load_cal()
        # create process id as sha256 hash of system time       
        self.pid = my_id
        # create T with all spots initialized to 0
        self.T = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        # create sqs object 
#        new_sqs = boto3.resource('sqs', 'us-east-2')

    ## load log and calendar from memory
    def load_cal(self):
        with open('Log.cal', 'r') as f:
            self.log = utils.string_to_struc(f.read())
            f.close()

        with open('Calendar.cal', 'r') as f:
            self.calendar = utils.string_to_struc(f.read())
            f.close()


    ## incriments clock and correct spot in self.T
    def inc_clock(self):
        self.clock += 1
        self.T[self.pid][self.pid] = self.clock

    ## adds event to log updates calendar
    ## @param a_r - add or remove can either be 0(add) or 1(remove)
    ## @param event - event in calendar to be added or removed
    def add_to_log(self, a_r, event):
        # incriment clock every time entry is created
        self.inc_clock()

        self.log[a_r + str(self.pid) + str(self.clock).zfill(3)] = [event, self.T]
        self.update_calendar()
        with open('Log.cal', 'r+') as f:
            text = utils.struc_to_string(self.log)
            f.write(text)
            f.truncate()
            f.close()

        with open('Calendar.cal', 'r+') as f:
            text = utils.struc_to_string(self.calendar)
            f.write(text)
            f.truncate()
            f.close()

    ## updates calendar according to log
    def update_calendar(self):
        add = []
        remove = []
        # clear calendar
        self.calendar = []
        # iterate over log to get calendar events
        for logid in self.log.keys():
            # if add event, append to add list
            if logid[:1] == '0':
                add.append(self.log[logid][0])
            # else, is remove and append to remove
            else:
                remove.append(self.log[logid][0])
        for event in add:
            if event not in remove:
                self.calendar.append(event)
        return

    ## deletes entry with that entry id
    ## @param uid - id of user who created the event
    ## @param c_val - clock value of user who created the event
    def remove_from_calendar(self, name):
        name = name.lower()
        for event in self.calendar:
            if name.lower() == event[0].lower():
                # add delete event to log
                self.add_to_log('1', event)
                # update calendar
                self.update_calendar()
                print('Removed', name, 'from calendar.\nHere is what the calendar looks like so far:')
                self.print_calendar()
                # add remove event to log
                print()
                return
        print('Failed to remove', name, 'from calendar.\nHere is what the calendar looks like so far:')
        self.print_calendar()
        print()
        return False

    ## turn start day/time and end day/time to valid log entry 
    ## @param name - name of appointment
    ## @param day - starting day of entry
    ## @param s_time - starting time of entry
    ## @param e_time - ending day of entry
    ## @param p_L - list of processes involved
    def create_entry(self, name, day, s_time, e_time, p_L):
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
            # first entry in log is 5 digits where first is the 
            # '0' for add event or '1' for remove event, the second is
            # creator and the last 3 are the clock value of that event 
            creator = int(entry[1:2])
            created_at = int(entry[2:])
            # if created at time is smaller than entry in T
            if self.T[to_id][creator] < created_at:
                # add entry to new truncated log
                send_log[entry] = self.log[entry]

    ## adds entry to log
    ## @param entry - entry to be entered into log
    def add_to_calendar(self, entry):
        # if calendar is empty, add it (update calendar makes sure
        # calendar is correct)
        if not self.calendar:
            self.add_to_log('0', entry)
            return True

        # if calendar is not empty, check events in calendar
        for event in self.calendar:
            # check to see if name is unique
            if event[0] == entry[0]:
                print('There is already an entry in the log with this name.')
                return False
            # if it doesn't already exist, add it to log
            # check iterate over all involved processes in new entry
            for p in entry[4]:
                # if an involved process is also in the event check to see if
                # events overlap
                if p in event[4]:
                    # if start time of new is before end time of old
                    # and end time of new is after start time of old, they overlap
                    if entry[2] < event[3] and entry[3] > event[2]:
                        print('There is a conflict with process', p, '.\n', entry[0], 'will not be added.')
                        self.break_tie(entry, event)
                        # return false because log will be handled in break_tie
                        return
        # if there are no collisions, add to log
        self.add_to_log('0', entry)

    ## checks T matrix in log for which process came first,
    ## if T matrix can't decide, use EID
    ## @param entry - new entry to be decided if saved or not
    def break_tie(self, new, old):
        self.add_to_log('0', new)
        if new[1] < old[1]:
            print(old, 'lost tie to', new)
            self.remove_from_calendar(old[0])
        else:
            print(new, 'lost tie to', old)
            self.remove_from_calendar(new[0])

    ## prints contents of log
    def print_log(self):
        if not self.log:
            print('Nothing in log.')
            return
        for lid in self.log.keys():
            print('log entry', lid + ':')
            print(self.log[lid])

    ## prints contents of calendar
    ## @param everyone - parameter for deciding to print all calendar
    ##      events or just the events involving this process
    def print_calendar(self, everyone=True):
        empty = True
        for event in self.calendar:
            if everyone or self.pid in event[4]:
                empty = False
                utils.print_entry(event)
        if empty:
            print('Nothing in calendar.')
        
    ## creates calendar event, adds it to log, and sends update message to everyone
    ## @param name - name of event
    ## @param day - starting day of entry
    ## @param s_time - starting time of entry
    ## @param e_time - ending time of entry
    ## @param p_L - list of processes involvedlj
    def add_event(self, name, day, s_time, e_time, p_L):
        event = self.create_entry(name, day, s_time, e_time, p_L)
        if self.add_to_calendar(event):
            print('Added event to calendar.\nHere is what the calendar looks like so far:')
        self.print_calendar(True)
        print()

    ## runs simple demo of calendar
    def demo_cal(self):

        entry = cal.create_entry('Event1', 'Tuesday', '2:00', '6:00', [0,1,2,] )
        print('adding entry', entry)
        cal.add_to_calendar(entry)
        eid = entry[0]

        entry = cal.create_entry('Event2', 'Wednesday', '12:00', '12:30', [0,2] )
        cal.add_to_calendar(entry)

        entry = cal.create_entry('Event3', 'Sunday', '2:00', '6:00', [1,3] )
        cal.add_to_calendar(entry)
        
        entry = cal.create_entry('Event4', 'Thursday', '2:00', '6:00', [1,3] )
        cal.add_to_calendar(entry)

        entry = cal.create_entry('Event5', 'Thursday', '2:00', '6:00', [1,3] )
        cal.add_to_calendar(entry)

        # print log
        print('log before remove:')
        self.print_log()
        # remove from log and print again
        self.remove_from_calendar('Event2')

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
    if len(sys.argv) == 1:
        cal.demo_cal() 
    elif sys.argv[1] == '-l':
        cal = Calendar(new_session=False)
        print("Loaded log:")
        cal.print_log()
        print("Loaded calendar:")
        cal.print_calendar()
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

