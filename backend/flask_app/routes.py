from flask import request
from flask_app import (
    app, dates, airlines, carriers, tracker, exceptions, httpstatus, messenger
)


@app.route('/form', methods=['GET'])
def get_form_start_data():
    date_options = dates.get_date_options()
    airline_options = list(airlines.airline_codes)
    carrier_options = list(carriers.carrier_codes)
    return(
        {
            'carriers': carrier_options,
            'dates' : date_options,
            'airlines' : airline_options
        })

@app.route('/register-new', methods=['POST'])
def register_new():
    form = request.get_json()
    try:
        tracker.register_new_tracking(**form)
        return httpstatus.codes['success']
    except exceptions.MissingFlight:
        return  httpstatus.codes['missing']
    except exceptions.DuplicateTrackingInformation:
        return  httpstatus.codes['duplicate']
    except Exception as e:
        messenger.send(e)
    
    