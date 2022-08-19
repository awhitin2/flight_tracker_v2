import telegram
from twilio.rest import Client
from flask_app import credentials, models, dates



account_sid = credentials.TWILIO_SSID
auth_token = credentials.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

TWILIO_NUMBER = '+16672222362'


def send_update(flight:models.Flight, changes)->None:
    body = _format_update_message(flight, changes)
    _send_sms(flight, body)

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
    body = (
            f'Flight {flight.airline_code} {flight.number} has arrived!\n\n'
            f'Status:\n'
            f"{_format_arrival_status(flight, changes)}\n\n"
            'You will no longer receive updates. Thanks for hanging out!'
        )
    _send_sms(flight, body)

def _format_arrival_status(flight: models.Flight, changes: dict[str, dict[str:str]]):
    scheduled = flight.scheduled_arrival_time
    actual = changes['estimated_arrival_time']['updated']
    delayed, hours, minutes = dates.calculate_arrival_delta(scheduled, actual)
    status = 'behind schedule' if delayed else 'ahead of schedule'
    hours_str = f'{str(int(hours))} hours, ' if hours else ''
    minutes_str = f'{str(int(minutes))} minutes' if minutes else ''

    return f'Arrived {hours_str}{minutes_str} {status}'


def send_registration_confirmation(user: models.User, flight: models.Flight)->None:
    body = (
        f'Welcome to Flight Tracker! You will now recieve notifications for any '
        f'changes to {flight.airline} flight {flight.airline_code} {flight.number} '
        f'departing on {flight.date_str}'
    )
    _send_sms(flight, body, recipient = user)

# I dont' like this

def _send_sms(flight: models.Flight, body: str, recipient = None):
    try:
        if recipient:
            client.messages.create(to = '+1'+recipient.cell, body=body, from_=TWILIO_NUMBER)
        else:
            for recipient in flight.followers:
                client.messages.create(to = '+1'+recipient.cell, body=body, from_=TWILIO_NUMBER)
    except KeyError as e:
        send_telegram(e)
    

def send_telegram(body: str):
    bot = telegram.Bot(token=credentials.TELEGRAM_TOKEN)
    bot.send_message(chat_id = credentials.TELEGRAM_ID, text = body)