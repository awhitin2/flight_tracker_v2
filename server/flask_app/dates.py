import datetime

#Consider timezone support

def get_date_options():
    today = datetime.date.today()
    date_objs = [today + datetime.timedelta(days=i) for i in range(3)]
    return [date.strftime('%m/%d/%Y') for date in date_objs]

def calculate_arrival_delta(scheduled: str, actual: str)->tuple:
    scheduled = scheduled.split()[0]
    scheduled = datetime.datetime.strptime(scheduled,'%H:%M')
    actual = actual.split()[0]
    actual = datetime.datetime.strptime(actual,'%H:%M')
    delta = scheduled-actual
    minutes = delta.total_seconds()/60
    delayed = minutes < 0
    hours, minutes = divmod(abs(minutes), 60)
    return delayed, hours, minutes

def convert_to_str(date_obj):
    return date_obj.strftime('%m/%d/%Y')

def convert_to_date_obj(date_str):
    return datetime.datetime.strptime(date_str,'%m/%d/%Y')
