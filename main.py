from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from dotenv import load_dotenv
import requests as rq
from pprint import pprint


man = DataManager()
search=FlightSearch()
sheet_dat = man.sheet_data

for entry in sheet_dat:
    if not entry['iataCode']:
        entry['iataCode'] = search.get_cities(entry['city'])
        man.update_sheet(entry)





