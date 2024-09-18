from dotenv import load_dotenv
import os
import requests as rq
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.search_endpoint = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        load_dotenv()
        self.apikey = os.getenv('FLIGHT_API_KEY')
        self.apisecret = os.getenv('FLIGHT_API_SECRET')
        self.headers = {}
        self.get_token()

    def get_token(self):
        access_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        tokheaders = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        tokdata = f'grant_type=client_credentials&client_id={self.apikey}&client_secret={self.apisecret}'
        tok = rq.post(access_endpoint, headers=tokheaders, data=tokdata)
        tok.raise_for_status()
        jtok=tok.json()
        self.headers ={
            "Authorization" : f"{jtok['token_type']} {jtok['access_token']}",
        }

    def get_cities(self, q:str):
        cities_endpoint = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
        param = {
            "keyword": q
        }
        cities = rq.get(cities_endpoint, headers=self.headers, params=param)
        cities.raise_for_status()
        return cities.json()['data'][0]['iataCode']


