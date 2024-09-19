from data_manager import DataManager
from flight_data import *
from flight_search import FlightSearch
from notification_manager import *
from dotenv import load_dotenv
import requests as rq
from pprint import pprint

ORIGIN = "LON"
CURRENCY = "GBP"
man = DataManager()
search=FlightSearch()
sheet_dat = man.sheet_data

changes = False
for entry in sheet_dat:
    if not entry['iataCode']:
        entry['iataCode'] = search.get_cities(entry['city'])
        man.update_sheet(entry)
        changes = True
if changes:
    man.read_sheet()

cheapcheap = []
for destination in sheet_dat:
    flights=search.search_flights(ORIGIN, destination['iataCode'], CURRENCY)
    cheapcheap.append(find_cheap(destination['city'], destination['lowestPrice'], flights))

low_send(cheapcheap, CURRENCY)
