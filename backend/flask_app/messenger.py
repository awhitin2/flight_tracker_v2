from flask_app import credentials
import yagmail

from flask_app import models
from flask_app.carriers import carrier_codes

yag = yagmail.SMTP(credentials.EMAIL_ACCOUNT, credentials.EMAIL_PASSWORD)


import telegram

def send_t_update(flight: models.Flight, changes: dict[str, dict[str:str]]):
    bot = telegram.Bot(token=credentials.TELEGRAM_TOKEN)
    message = _format_message(flight, changes)
    bot.send_message(chat_id = credentials.TELEGRAM_ID, text = message)
    pass


def _format_message(flight: models.Flight, changes: dict[str, dict[str:str]]):
    content = [f'Updates for {flight.airline} flight {flight.airline_code} {flight.number}:\n']

    for k, v in changes.items():
        change = k.replace('_', ' ')\
                  .capitalize()
        content.extend([
            f'{change}:', 
            f"Previous: {v['old']} --> Updated: {v['updated']}\n"
        ])
    return '\n'.join(content)


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
