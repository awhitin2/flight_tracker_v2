import smtplib
from email.message import EmailMessage
from dataclasses import dataclass

import credentials

@dataclass
class SMS:
    number: str
    gateway: str
    subject: str
    body: str

    @property
    def recipient(self) -> str:
        return self.number + self.gateway

class Messenger:

    def __init__(
        self, username: str, password: str, conn: smtplib.SMTP = None) -> None:
        
        self.username = username
        self.password = password
        self.conn = conn

    def open_conn(self):
        # CREATE CONNECTION TO SMTP SERVICE
        self.conn = smtplib.SMTP("smtp.gmail.com",587)
        self.conn.ehlo()
        self.conn.starttls()
        self.conn.ehlo
        self.conn.login(self.username, self.password)

    def close_conn(self):
        # CLOSE CONNECTION TO SMTP SERVICE
        self.conn.close()

    def send_sms(self, msg, one_time=False):
        if one_time:
            self.open_conn()

        # CREATE MESSAGE
        message = EmailMessage()
        message.set_content(msg.body)
        message["From"] = self.username
        message["To"] =  msg.recipient
        message.add_header('Subject', msg.subject)
        # SEND MESSAGE
        self.conn.sendmail(self.username, msg.recipient, message.as_string(unixfrom=True))

        if one_time:
            self.close_conn()

content = (
            f'Flight F10 202 has arrived!\n\n'
            f'Status:\n'
            f"Arrived on time.\n\n"
            'You will no longer receive updates. Thanks for hanging out!'
        )

# message = EmailMessage()
# message.set_content(content)
# message["From"] = credentials.EMAIL_ACCOUNT
# message["To"] =  '2407609543@tmomail.net'
# message.add_header('Subject', 'This is my subject')

# server = smtplib.SMTP( "smtp.gmail.com", 587 )
# server.starttls()
# server.login( credentials.EMAIL_ACCOUNT, credentials.EMAIL_PASSWORD )
# server.sendmail( credentials.EMAIL_ACCOUNT, '2407609543@tmomail.net', message.as_string(unixfrom=True) )


if __name__ == '__main__':
    content = (
            f'Flight F10 202 has arrived!\n\n'
            f'Status:\n'
            f"Arr unixfrom = True.\n\n"
            'You will no longer receive updates. Thanks for hanging out!'
        )
    msg = SMS('2407609543', '@tmomail.net', 'Flight Tracker Update', content)
    my_messenger = Messenger(credentials.EMAIL_ACCOUNT, credentials.EMAIL_PASSWORD)
    my_messenger.send_sms(msg, one_time=True)