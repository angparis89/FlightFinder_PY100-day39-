from dotenv import load_dotenv
import os
import requests as rq
from datetime import datetime, timedelta
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
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
        print(f"Status code {cities.status_code}. Airport IATA: {cities.text}")
        try:
            code = cities.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {q}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {q}.")
            return "Not Found"
        return code

    def search_flights(self, orig:str, dest:str, cur:str):
        search_endpoint = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        from_time = datetime.now() + timedelta(days=1)
        to_time = datetime.now() + timedelta(weeks=26)
        search_param = {
            "originLocationCode": orig,
            "destinationLocationCode": dest,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": cur,
            "max": "10",
        }
        flights = rq.get(search_endpoint, headers=self.headers, params=search_param)
        if flights.status_code != 200:
            print(f"check_flights() response code: {flights.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", flights.text)
            return None
        return flights.json()