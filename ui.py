import calendar
import utils

class ui:

    ## @param cal - calendar object that will be interated with
    def __init__(self, cal):
        self.cal = cal
        # variables for creating a new event
        self.s_day = ''
        self.s_time = ''
        self.e_day = ''
        self.e_time = ''
        self.processes_L = set()
    
        # variables for deleting an event
        self.d_uid = -1
        self.d_number = -1

    ## main ui loop
    def run(self):  
        # value to read input into 
        val = ''

        print('Type q to exit.\nWould you like to add or remove a calendar event?')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(add/remove) > ').lower()

            # adding process
            if val == 'add':
                val = self.get_s_day()
                print('exited add')
            if val == 's_time' and self.s_day != '':
                val = self.get_s_time()
            if val == 'e_day' and self.s_time != '':
                val = self.get_e_day()
            if val == 'e_time' and self.e_day != '':
                val = self.get_e_time()
            if val == 'processes' and self.e_time != '':
                val = self.get_processes()
            if val == 'add' and self.e_time != '':
                # when we get all of our info, add an event
                self.cal.add_event(list(self.processes_L), self.s_day, self.s_time, self.e_day, self.e_time)
                # clear event info
                self.s_day = ''
                self.s_time = ''
                self.e_day = ''
                self.e_time = ''
                self.processes_L = set()

            if val == 'remove':
                val = self.get_uid()         
            if val == 'number' and self.d_uid > -1:
                val = self.get_number()
            if val == 'remove' and self.d_number > -1:
                self.cal.remove_from_log(self.d_uid, self.d_number)
        
    ## method to check for valid time
    ## @param time - string to check as valid day
    ## @param end - boolean for if end time
    def check_time(self, time, end=False):
        hour, minute = time.split(':')
        # if this is an end time and is on same day as start, make sure it comes after start
        if end and utils.convert_day(self.s_day) == utils.convert_day(self.e_day):
            s_hour, s_minute = self.s_time.split(':')
            if int(hour) < int(s_hour):
                print('End time must come after start time')
                return False
            elif int(hour) == int(s_hour) and int(minute) < int(minute):
                print('End time must come after start time')
                return False
        # make sure hour is less than 24 (valid)
        if int(hour) < 24: 
            if int(minute) == 30 or int(minute) == 0:
                return True
            else:
                print('Appointments can only be scheduled on the hour or on the 30')
        return False

    ## method to check for valid day
    ## @param day - string to check if is valid day
    ## @param end - boolean for if end day
    def check_day(self, day, end=False):
        day = day.lower()

        # if ending day, make sure it comes after start day
        if end:
            if utils.convert_day(day) < utils.convert_day(self.s_day):
                print('End day must come after start day.')
                return False

        # return true if valid day
        if day == 'monday':
            return True
        elif day == 'tuesday':
            return True
        elif day == 'wednesday':
            return True
        elif day == 'thursday':
            return True
        elif day == 'friday':
            return True
        elif day == 'saturday':
            return True
        elif day == 'sunday':
            return True
        return False
    
    ## ui loop for inputting 
    def get_number(self):
        val = ''
        print('What is the event number of the even you would like to delete? (Enter cancel to cancel.)')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(some number/cancel) > ').lower()
            if val == 'cancel':
                return ''
            # lazy way to check to see if it is a number
            if int(val) < 10000: 
                self.d_number = int(val)
                return 'remove'
        return val

    ## ui loop for inputting start time
    def get_uid(self):
        val = ''
        print('Who created the event you would like to delete? (Enter cancel to cancel.)')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(0/1/2/3/cancel) > ').lower()
            if val == 'cancel':
                return ''
            if int(val) < 4: 
                self.d_uid = int(val)
                return 'number'
        return val
    
    ## ui loop for inputting start time
    def get_s_time(self):
        val = ''
        print('What time does this appointment start? (Enter cancel to cancel.)')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(hh:mm/cancel) > ').lower()
            if val == 'cancel':
                self.s_day = ''
                self.s_time = ''
    
    ## ui loop for inputting start time
    def get_s_time(self):
        val = ''
        print('What time does this appointment start? (Enter cancel to cancel.)')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(hh:mm/cancel) > ').lower()
            if val == 'cancel':
                self.s_day = ''
                self.s_time = ''
                self.e_day = ''
                self.e_time = ''
                self.processes_L = set()
                return ''
            if self.check_time(val): 
                self.s_time = val
                return 'e_day'
        return val

    # ui loop for inputting start time
    def get_e_time(self):
        val = ''
        print('What time does this appointment start? (Enter cancel to cancel.)')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(hh:mm/cancel) > ').lower()
            if val == 'cancel':
                self.s_day = ''
                self.s_time = ''
                self.e_day = ''
                self.e_time = ''
                self.processes_L = set()
                return ''
            if self.check_time(val): 
                self.e_time = val
                return 'processes'
        return val
    
    # ui loop for inputting a start day
    def get_s_day(self):
        val = ''
        print('What day does this appointment start? (Enter cancel to cancel.)')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(Monday-Sunday/cancel) > ').lower()
            if val == 'cancel':
                self.s_day = ''
                self.s_time = ''
                self.e_day = ''
                self.e_time = ''
                self.processes_L = set()
                return ''
            if self.check_day(val): 
                self.s_day = val
                return 's_time'
        return val    

    # ui loop for inputting a start day
    def get_e_day(self):
        val = ''
        print('What day does this appointment end? (Enter cancel to cancel.)')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(Monday-Sunday/cancel) > ').lower()
            if val == 'cancel':
                self.s_day = ''
                self.s_time = ''
                self.e_day = ''
                self.e_time = ''
                self.processes_L = set()
                return ''
            if self.check_day(val): 
                self.e_day = val
                return 'e_time'
        return val

    def get_processes(self):
        val = ''
        print('Who is going to this appointment? (Enter e when done/cancel to cancel.)')
        while val != 'q' and val != 'quit' and val != 'exit':
            val = input('(0/1/2/3/e/cancel) > ').lower()
            if val == 'cancel':
                self.s_day = ''
                self.s_time = ''
                self.e_day = ''
                self.e_time = ''
                self.processes_L = set()
                return ''
            # if we see an e, return
            if val == 'e' and self.processes_L:
                return 'add'
            elif val == 'e':
                print('You must enter at least one participant')
            if int(val) < 4: 
                print('Adding', val, 'to event.')
                self.processes_L.add(int(val))
        return val
        
