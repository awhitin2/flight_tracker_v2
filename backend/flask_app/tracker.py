import requests
import bs4
import datetime
from flask_app import db, dates, models, airlines, exceptions, messenger
from flask_app import database as my_db


FLIGHT_STATS_BASE_URL = 'https://www.flightstats.com/v2/flight-tracker'
FLIGHT_INFO_PATH = 'flight_tracker/flight_info.json'


def register_new_tracking(
        airline: str, flight_number: str,  date: str, cell: str
    )->None:

    existing_flight = True
    existing_user = True
    airline_code = airlines.airline_codes[airline]

    flight = my_db.get_flight(airline_code, flight_number, date)
    if not flight:
        existing_flight = False
        flight = _register_new_flight(airline_code, flight_number, date)
        db.session.add(flight)
        
    user = my_db.get_user_(cell)
    if not user:
        existing_user = False
        user = my_db.set_user(cell)
        db.session.add(user)

    if existing_flight and existing_user:
        raise exceptions.DuplicateTrackingInformation

    user.flights.append(flight)
    db.session.commit()
    messenger.send_registration_confirmation(user, flight)

def _register_new_flight(airline_code:str, flight_number:str, date:str)->models.Flight:
    flight_info = get_flight_info(airline_code, flight_number, date)
    flight = my_db.set_flight(flight_number, airline_code, date, flight_info)
    return flight

def get_flight_info(airline_code:str, flight_number:str, date:str)->dict[str:str]:
    try:
        soup = _get_soup(airline_code, flight_number, date)
        return _extract_flight_info(soup)
    except exceptions.MissingFlight as e:
        raise e

def _get_soup(airline_code:str, flight_number:str, date:str)->bs4.BeautifulSoup:

    date_obj = dates.convert_to_date_obj(date)

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

def _extract_flight_info(soup: bs4.BeautifulSoup)-> dict[str:str]:

    data = [tag.text for tag in soup.select(
        ("div.ticket__TicketContainer-sc-1rrbl5o-0 "
        "div.text-helper__TextHelper-sc-8bko4a-0"))]
    
    status = '' ## Check for arrived status. Send Arrival notification and then stop notifications
    if data:
        flight_info = {
            "airline": data[1],
            "scheduled_departure_time": data[14],
            "estimated_departure_time": data[16],
            "departure_airport": data[2],
            "scheduled_arrival_time": data[27],
            "estimated_arrival_time": data[29],
            "arrival_airport": data[4],
            "status": f'{data[6]}: {data[7]}'
        }
        return flight_info
    raise exceptions.MissingFlight

# register_new_tracking(airline_code, flight_no, date, '8189189', 'T-Mobile')

