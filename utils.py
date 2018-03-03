import math
import json

## turn day (monday-sunday)
## to number (000 - 600)
## @param day - string representing a day
def convert_day(day):
    # convert day string to all lowercase
    day = day.lower()

    # map day to number
    if day == 'monday':
        return 0
    elif day == 'tuesday':
        return 100
    elif day == 'wednesday':
        return 200
    elif day == 'thursday':
        return 300
    elif day == 'friday':
        return 400
    elif day == 'saturday':
        return 500
    elif day == 'sunday':
        return 600
    elif day == '0':
        return 'Monday'
    elif day == '1':
        return 'Tuesday'
    elif day == '2':
        return 'Wednesday'
    elif day == '3':
        return 'Thursday'
    elif day == '4':
        return 'Friday'
    elif day == '5':
        return 'Saturday'
    elif day == '6':
        return 'Sunday'

## convert hours and minutes to a number between 0 and 47
## where 2:00 (military time) is 4 ## and 16:30 is 33
## @param time - string time in format hh:mm
def convert_time(time):
    # get hours and minuts from string time
    hour, minute = time.split(':')

    # multiply hour by 2
    time = int(hour) * 2
    # add 1 if minute is 30
    time += int(minute) / 30

    # return time as an integer
    return int(time)

## convert time value of int 0-47
## to string time in format hh:mm
## @param time - int value 0-47
def format_time(time):
    # get hour by getting floor of time/2
    formatted = str(int(int(time)/2))
    # get minutes by checking if even or odd
    if (int(time) % 2) == 1:
        formatted += ':30'
    else:
        formatted += ':00'

    return formatted

## calculate duration given two times
## in 0-47 format
## @param s_time - starting time
## @param e_time - ending time
def calc_duration(s_time, e_time):
    duration = int(e_time) - int(s_time)
    days = int(duration / 100)
    hours = int(duration / 2) 
    minutes = (duration % 2) * 30
  
    # if appointment is more than a day
    if duration > 47:
        # get hours remaining in s_time day
        hours = (48 - (int(s_time) % 100)) / 2
        # add above to hours since e_time day started
        hours += (int(e_time) % 100) / 2
        # add 24 hours four each additional day
        hours = int(hours + days * 24)

    # create duration string
    duration = (str(hours) + ' hours ' + str(minutes) + ' minutes')
 
    return duration

## print entry in human readable format
## @param entry - calendar entry in format
## [entryID, [involved process ID's], startTime, endTime]
def print_entry(entry):
    # convert first digit of time to a day 
    s_day = convert_day(entry[2][0])
    e_day = convert_day(entry[3][0])

    # convert last two digits of time to time 
    s_time = format_time(entry[2][1:]) 
    e_time = format_time(entry[3][1:])

    # get duration of entry
    duration = calc_duration(entry[2], entry[3])

    print('\nEntry ID:', entry[0])
    print('Appointment with')
    for process in entry[1]:
        print('\t', process)
    print('From', s_day, 'at', s_time)
    print('To', e_day, 'at', e_time)
    print('For', duration)

## convert some datastructure to a string
## I made this because I can never remember
## if I should use dumps or loads
## @param struc - some structure to be converted to a string
def struc_to_string(struc):
    return json.dumps(struc)

## convert some string to a structure
## I made this because I can never remember
## if I should use dumps or loads
## @param string - some structure to be converted to a string
def string_to_struc(string):
    return json.loads(string)

## prints T matrix
## @param T - matric to be printed   
def print_T(T):
    for i in range(len(T)):
        for j in range(len(T[0])):
            print(' ', T[i][j], end='')
        print()
 
## takes in two T matrices and
## updates first one so that it
## is up to date with the second
## T matrix
## @param my_T - local T that needs to be updated
## @parma rec_T - T that was received in message that 
##      should be used to update local T
def update_T(my_T, rec_T, my_id):
    print('my_T:')
    print_T(my_T)
    print('rec_T:')
    print_T(rec_T)

    new_T = my_T
    # update my row
    for i in range(len(my_T)):
        # check rows that are not mine
        if i != my_id:
            for j in range(len(my_T[0])):
                # if we find a new largest value, update
                if new_T[my_id][j] < rec_T[i][j]:
                    new_T[my_id][j] = rec_T[i][j] 
                # fill spots not in my row with largest value
                if new_T[i][j] < rec_T[i][j]:
                    new_T[i][j] = rec_T[i][j]   
 
    print('after update:\nmy_T:')
    print_T(new_T)
    return new_T


