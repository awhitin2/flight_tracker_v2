import requests
import bs4
import datetime
from flask_app import db, dates, models, airlines
from flask_app import database as my_db



FLIGHT_STATS_BASE_URL = 'https://www.flightstats.com/v2/flight-tracker'
FLIGHT_INFO_PATH = 'flight_tracker/flight_info.json'

flight_no = "220"
date = "08/16/2022"
airline_code = 'DL'

def register_new_tracking(
    airline: str, flight_number: str,  date: str, cell: str, carrier: str
)->str:
    airline_code = airlines.airline_codes[airline]
    flight = my_db.get_flight(airline_code, flight_number, date)
    if not flight:
        flight = _register_new_flight(airline_code, flight_number, date)
        db.session.add(flight)
        
    user = my_db.get_user_(cell)
    if not user:
        user = my_db.set_user(cell, carrier)
        db.session.add(user)

    user.flights.append(flight)
    db.session.commit()

    return("Flight successfully registered")

def _register_new_flight(airline_code:str, flight_number:str, date_str:str)->models.Flight:
    soup = _get_soup(airline_code, flight_number, date_str)
    flight_info = _extract_flight_info(soup)
    flight = my_db.set_flight(flight_no, airline_code, date, flight_info)
    return flight

def _get_soup(airline_code:str, flight_number:str, date_str:str)->bs4.BeautifulSoup:

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
            "arrival_airport": data[4]
        }

        return flight_info
    else: 
        raise ValueError('Flight not Found')

# register_new_tracking(airline_code, flight_no, date, '8189189', 'T-Mobile')

