import requests
import bs4
import datetime
import json
import telegram
import os
import dates

FLIGHT_STATS_BASE_URL = 'https://www.flightstats.com/v2/flight-tracker'
FLIGHT_INFO_PATH = 'flight_tracker/flight_info.json'


def get_html(airline_code, flight_number, date_str):

    date_obj = dates.convert_to_date_obj(date_str)

    url = _format_url(airline_code, flight_number, date_obj)
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.content, 'html.parser')
    return(soup)


def _format_url(airline_code: str, flight_number: str, date_obj: datetime.date)->str:
    url = (
        f'{FLIGHT_STATS_BASE_URL}/{airline_code}/{flight_number}'
        f'/?year={date_obj.year}&month={date_obj.month}&date={date_obj.day}'
    )
    return url

def extract_flight_info(soup: bs4.BeautifulSoup)-> dict[str:str]:

    data = [tag.text for tag in soup.select(
        ("div.ticket__TicketContainer-sc-1rrbl5o-0 "
        "div.text-helper__TextHelper-sc-8bko4a-0"))]
    
    status = '' ## Check for arrived status. Send Arrival notification and then stop notifications

    flight_info = {
        "flight_number": data[0],
        "airline": data[1],
        "scheduled_departure_time": data[14],
        "estimated_departure_time": data[16],
        "departure_airport": data[2],
        "scheduled_arrival_time": data[27],
        "estimated_arrival_time": data[29],
        "arrival_airport": data[4]
    }

    return flight_info

def _get_stored_info():
     with open(FLIGHT_INFO_PATH, "r") as file:
        return json.loads(file.read())

def _send_message(new_info:dict, stored_info:dict)->None:
    
    changes = ''
    changed_info = ''
    if new_info['estimated_departure_time'] != stored_info['estimated_departure_time']:
        changes = "estimated departure"
        changed_info = (
            f'\nPreviously estimated departure: {stored_info["estimated_departure_time"]}'
            f'\nCurrently estimated departure: {new_info["estimated_departure_time"]}'
        )

    if new_info['estimated_arrival_time'] != stored_info['estimated_arrival_time']:
        changed_info += (
            f'\nPreviously estimated arrival: {stored_info["estimated_arrival_time"]}'
            f'\nCurrently estimated arrival: {new_info["estimated_arrival_time"]}'
        )

        if not changes:
            changes += "estimated arrival"
        else:
            changes += "/arrival"

    
    message = (f'The {changes} of {stored_info["airline"]} flight '
        f'{stored_info["flight_number"]} '
        f'from {stored_info["departure_airport"]} to {stored_info["arrival_airport"]} '
        f'has changed. {changed_info} '
        )
        
    _telegram_notifier(message)

def _update_stored_info(new_info:dict)->None:
     with open(FLIGHT_INFO_PATH, "w") as file:
        file.write(json.dumps(new_info))

def _telegram_notifier(message: str):

    with open("flight_tracker/resources/telegram_dict.json", "r") as file:
        data = json.load(file)

    bot = telegram.Bot(token=data["TOKEN"])
    bot.send_message(chat_id = data["MY_ID"], text = message)
    
    return 1


def _update_flight_list(registration_info: dict):

    if os.stat(FLIGHT_INFO_PATH).st_size == 0: #Check if file is empty
        flight_list = []
    else:
        flight_list = _load_flight_list()

    flight_list.append(registration_info)
    _save_flight_list(flight_list)

def _load_flight_list()-> list:
    with open(FLIGHT_INFO_PATH, "r") as file:
        return json.loads(file.read())

def _save_flight_list(flight_list):
    with open(FLIGHT_INFO_PATH, "w") as file:
        file.write(json.dumps(flight_list))


def register_new_flight(
    airline_code: str, flight_number: str, 
    date_str: str, phone: str, carrier: str):
    
    soup = get_html(airline_code, flight_number, date_str)
    flight_info = extract_flight_info(soup)
    
    registration_info = {
        'search_info': {
            'airline_code' : airline_code,
            'flight_number' : flight_number,
            'date_str' : date_str,
        },
        'contact_info': {
            'phone': phone,
            'carrier': carrier
        },
        'flight_info': flight_info
    }

    _update_flight_list(registration_info)

    return("Flight successfully registered")

# airline_code = "F9"
# flight_number = "611"
# date_str = '07/14/2022'
# register_new_flight(airline_code, flight_number, date_str, '2839u423', 'T-mobile')

def _check_for_updates(flight):
    soup = get_html(**flight['search_info'])
    new_info = extract_flight_info(soup)
    old_info = flight['flight_info']
    if not new_info == old_info:
        _send_message(new_info, old_info)
        # _update_stored_info(new_info)

 
def main(): #Need to account for removing old flights
    os.chdir('/Users/andrewwhiting/Programming/flight_tracker_git/')
    flights = _load_flight_list()
    for flight in flights:
        _check_for_updates(flight) #Name that conveys also sending messages?
        #Updating stored info doesn't work here. 


if __name__ == '__main__':
    main()


''''
Necessary inputs:

Airline -- Derive airline_code from this
flight_number
date
cell number
cell carrier
'''