from dotenv import load_dotenv
import os
import requests as rq
from twilio.rest import Client

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self, price, dep_airport, ar_airport, out_date, in_date, cur):
        self.message = f"Low price alert! Only {price} {cur} to fly from {dep_airport} to {ar_airport}, on {out_date} until {in_date}."
        load_dotenv()
        self.sid = os.getenv('ACCOUNT_SID')
        self.auth = os.getenv('AUTH_TOKEN')
        self.from_m = os.getenv('FROM')
        self.to_m = os.getenv('TO')

def low_send(cheap, cur):
    msg_queue = []
    for cc in cheap:
        if cc.price != 'N/A':
            pr = cc.price
            dep = cc.origin_airport
            ar = cc.destination_airport
            out = cc.out_date.split('T')[0]
            inn = cc.return_date.split('T')[0]
            msg_queue.append(NotificationManager(pr, dep, ar, out, inn, cur))
    if not msg_queue:
        return
    else:
        for msg in msg_queue:
            client = Client(msg.sid, msg.auth)
            message = client.messages.create(
                body=msg.message,
                from_=msg.from_m,
                to=msg.to_m
            )
            print(message.status)

