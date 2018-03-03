

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
## where 2:00 (military time) is 4 
## and 16:30 is 33
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

def format_time(time):
    # get hour by getting floor of time/2
    formatted = str(int(int(time)/2))
    # get minutes by checking if even or odd
    if (int(time) % 2) == 1:
        formatted += ':30'
    else:
        formatted += ':00'

    return formatted

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
    duration = 0

    print('\nAppointment on', s_day, 'at', s_time, 'with:')
    for process in entry[1]:
        print(process)
    print('for', duration, 'ending on', e_day, 'at', e_time)

