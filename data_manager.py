from dotenv import load_dotenv
import os
import requests as rq

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheetendpoint = "https://api.sheety.co/2dbc372cf13232408a0f3dc10dc4a2ef/flightFinder/prices"
        load_dotenv()
        self.sheety_header = {
                "Authorization": f"Bearer {os.getenv('SHEETY_KEY')}",
            }
        self.sheet_data = self.read_sheet()
    def read_sheet(self):
        shet = rq.get(self.sheetendpoint, headers=self.sheety_header)
        shet.raise_for_status()
        return shet.json()["prices"]

    def update_sheet(self, row):
        ids = row["id"]
        upparam = {
            "price": {
                "city": row["city"],
                "iataCode": row["iataCode"],
                "lowestPrice": row["lowestPrice"],
            }
        }

        update_endpoint = self.sheetendpoint + f"/{ids}"
        upres = rq.put(update_endpoint, json=upparam, headers=self.sheety_header)
        upres.raise_for_status()