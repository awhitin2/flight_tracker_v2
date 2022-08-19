
from datetime import datetime
from flask_app import tracker, models, exceptions, messenger
from flask_app import database as my_db


def check_for_updates():
    flights = my_db.get_all_flights()
    change_count = 0
    flight_count = len(flights)
    for flight in flights:
        try:
            updated_info = tracker.get_flight_info(
                flight.airline_code,
                flight.number,
                flight.date_str
            )
        except exceptions.MissingFlight:
            print(f'Failed to find updated info for {flight.airline} {flight.number} from database')
            continue
        changes = _compare_info(flight, updated_info)
        if changes:
            change_count += len(changes)
            _process_changes(flight, changes)
        
    print(f"Script ran at {datetime.now()} and found {change_count} changes")
    if change_count:
        with open('flask_app/log.txt', 'a') as file:
            file.write(
                (f'{datetime.now()} -- status_checker checked\n' 
                f'{flight_count} flights and found {change_count} change(s)')
            )
    
def _compare_info(old_info: models.Flight, updated_info: dict[str: dict[str:str]])->dict:
    changes = {}
    for key, updated_value in updated_info.items():
        old_value = getattr(old_info, key)
        if not updated_value == old_value:
            if old_value == '--':
                old_value = 'None'
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
        messenger.send_update(flight, changes)
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