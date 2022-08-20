from flask import abort, render_template, request
from flask_app import (
    app, dates, airlines, tracker, exceptions, httpstatus, messenger
)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")


@app.route('/api/form', methods=['GET'])
def get_form_start_data():
    date_options = dates.get_date_options()
    airline_options = list(airlines.airline_codes)
    return(
        {
            'dates' : date_options,
            'airlines' : airline_options
        })

@app.route('/api/register-new', methods=['POST'])
def register_new():
    form = request.get_json()
    try:
        tracker.register_new_tracking(**form)
        return httpstatus.codes['success']
    except exceptions.MissingFlight:
        return  httpstatus.codes['missing']
    except exceptions.DuplicateTrackingInformation:
        return  httpstatus.codes['duplicate']
    except exceptions.InvalidCell:
        return httpstatus.codes['invalidCell']
    except Exception as e:
        messenger.send_telegram(str(e))
        return abort(404)
    
    