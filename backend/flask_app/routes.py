from flask_app import app, dates, airlines, carriers

@app.route('/form', methods=['GET'])
def get_form_start_data():
    date_options = dates.get_date_options()
    airline_options = list(airlines.airlines)
    carrier_options = list(carriers.carriers)
    return(
        {
            'carriers': carrier_options,
            'dates' : date_options,
            'airlines' : airline_options
        })