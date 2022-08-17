
from flask_app import tracker, models, exceptions, messenger
from flask_app import database as my_db



def check_for_updates():
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
    #Log?
    
def _compare_info(old_info: models.Flight, updated_info: dict[str: dict[str:str]])->dict:
    changes = {}
    for key, updated_value in updated_info.items():
        old_value = getattr(old_info, key)
        if not updated_value == old_value:  
            changes[key] = {
                'old': old_value,
                'updated': updated_value
            }
    return changes

def _process_changes(flight: models.Flight, changes: dict[str: dict[str:str]]):
    arrived = _check_arrived(changes)
    if arrived:
        messenger.send_arrived(flight, changes)
        my_db.delete_flight(flight)
    else:
        messenger.send_update(flight, changes, arrived)
        my_db.update_flight(flight, changes)
    

def _check_arrived(changes: dict[str: dict[str:str]]):
    if 'status' in changes:
        return 'Arrived' in changes['status']['updated']
    else:
        return False

def main():    
    check_for_updates()

if __name__ == '__main__':
    main()


# messenger.send_update_sms(flight.followers, flight, changes)