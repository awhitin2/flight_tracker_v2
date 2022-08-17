from flask_app import credentials, models
from flask_app.carriers import carrier_codes



def send_update(flight, changes, arrived=False)->None:
    message = _format_update_message(flight, changes)
    send(message)

def _format_update_message(flight: models.Flight, changes: dict[str, dict[str:str]]):
    content = [f'Update for {flight.airline} flight {flight.airline_code} {flight.number}:\n']

    for k, v in changes.items():
        change = k.replace('_', ' ')\
                  .capitalize()
        content.extend([
            f'{change}:', 
            f"Previous: {v['old']} --> Updated: {v['updated']}\n"
        ])
    return '\n'.join(content)

def send_arrived(flight: models.Flight, changes: dict[str, dict[str:str]])->None:
    message = (
            f'Flight {flight.airline_code} {flight.number} has arrived!\n\n'
            f'Status:\n'
            f"{changes['status']['updated']}\n\n"
            'You will no longer receive updates. Thanks for hanging out!'
        )
    send(message)

def send_registration_confirmation(user: models.User, flight: models.Flight)->None:
    message = (
        f'Welcome to Flight Tracker! You will now recieve notifications for any '
        f'changes to {flight.airline} flight {flight.airline_code} {flight.number} '
        f'departing on {flight.date_str}'
    )
    send(message)

def send(message):
    bot = telegram.Bot(token=credentials.TELEGRAM_TOKEN)
    bot.send_message(chat_id = credentials.TELEGRAM_ID, text = message)


# def send_update_sms(
#     users: list[models.User], 
#     flight: models.Flight, 
#     changes: dict[str, dict[str:str]]
#     )->None:
   
#     to = _construct_recipient_addresses(users)
#     subject = 'Flight Tracker Update'
#     message = Message(flight, changes)

#     yag.send(to, subject, contents = message.body)

def _construct_recipient_addresses(users: models.User):
    # return [f'{user.cell}{carrier_codes[user.carrier]}' for user in users]
    return f"{'2407500944'}{'@msg.fi.google.com'}"
