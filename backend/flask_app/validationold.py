import bs4
import enum

import phonenumbers

import tracker


class Status(enum.Enum):

    valid = 'valid'
    invalid_flight = 'invalid flight'
    invalid_cell = 'invalid cell'

def validate(submission):
    if not _flight_is_valid(**submission):
        return Status.invalid_flight

    if not _cell_is_valid(submission['phone']):
        return Status.invalid_cell
    
    return Status.valid
    

def _flight_is_valid(airline_code, flight_number, date_str, **args):
    soup = tracker.get_html(airline_code, flight_number, date_str)
    status = soup.find(class_= "layout-row__Title-sc-1uoco8s-4 kaIMhA").text
    if status == "Flight Status Not Available":
        return False
    return True


def _cell_is_valid(cell_number:str):
    if not cell_number:
        return False
    return True

    # cell_number = cell_number.strip()

    # if not cell_number[0] == '+':
    #     cell_number = '+'+cell_number
    #     try:
    #         cell_number = phonenumbers.parse(cell_number)
    #     except:
    #         print("failed")
        

    # cell_number = phonenumbers.parse(cell_number)
    # return phonenumbers.is_possible_number(cell_number)