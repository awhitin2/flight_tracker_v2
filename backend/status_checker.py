
# Checker
## Get list of flights from database
## Check for any changed info and message
## Delete old flights

# Messager
## Confirmation when registered
## Any status changes
## Boarding/departure
## Arrival

from flask_app import tracker, models, exceptions, messenger
from flask_app import database as my_db


def _check_for_updates():
    flights = my_db.get_all_flights()
    for flight in flights:
        try:
            updated_info = tracker.get_flight_info(
                flight.airline_code,
                flight.number,
                flight.date_str
            )
        except exceptions.MissingFlight:
            print('Failed to find updated info for flight X from database')
            print('Send via telegram')
            continue
        changes = _compare_info(flight, updated_info)
        if changes:
            _process_changes(flight, changes)
            print(f'send message for {flight.airline_code}{flight.number}')
    print('No changes')
    #Log?
    
def _compare_info(old_info: models.Flight, updated_info: dict[dict[str:str]])->dict:
    changes = {}
    for key, updated_value in updated_info.items():
        old_value = getattr(old_info, key)
        if not updated_value == old_value:  
            changes[key] = {
                'old': old_value,
                'updated': updated_value
            }
    return changes

def _process_changes(flight: models.Flight, changes: dict[dict[str:str]]):
    messenger.send_t_update(flight, changes)
    # my_db.update_flight(flight, changes)
    
    #Update database
    #Delete old records

    pass

def main():
    _check_for_updates()

if __name__ == '__main__':
    main()


# messenger.send_update_sms(flight.followers, flight, changes)