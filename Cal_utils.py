

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
    print('hour:', hour, 'minute:', minute)

    return int(time) 
    


