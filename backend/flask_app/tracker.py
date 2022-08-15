import requests
import bs4
import datetime
from flask_app import db, dates, models


FLIGHT_STATS_BASE_URL = 'https://www.flightstats.com/v2/flight-tracker'
FLIGHT_INFO_PATH = 'flight_tracker/flight_info.json'

flight_no = "536"
date = "08/15/2022"
airline_code = 'F9'

def register_new_flight(
    airline_code: str, 
    flight_number: str, 
    date_str: str, 
    cell: str, 
    carrier: str
):
    
    soup = _get_html(airline_code, flight_number, date_str)
    flight_info = _extract_flight_info(soup)
    
    flight_db_obj = models.Flight(
        number = flight_number,
        airline_code = airline_code,
        date_str = date_str,
        airline = flight_info['airline'],
        scheduled_departure_time = flight_info['scheduled_departure_time'],
        scheduled_arrival_time = flight_info['scheduled_arrival_time'],
        estimated_arrival_time = flight_info['estimated_arrival_time'],
        arrival_airport = flight_info['arrival_airport'],
        # arrived = flight_info['arrived_status']
    )

    #check if user exists first
    user_db_obj = models.User(
        cell = cell,
        carrier = carrier
    )

    user_db_obj.flights.append(flight_db_obj)

    db.session.add_all([user_db_obj, flight_db_obj])
    db.session.commit()

    return("Flight successfully registered")

def _get_html(airline_code, flight_number, date_str):

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


def _check_for_updates(flight):
    soup = _get_html(**flight['search_info'])
    new_info = _extract_flight_info(soup)
    old_info = flight['flight_info']


# if __name__ == '__main__':
db.create_all()
register_new_flight(airline_code, flight_no, date, '309189', 'T-Mobile')

