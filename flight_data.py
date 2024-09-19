class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, city, pri, origin, destination, outday, retday):
        self.dest_city = city
        self.price = pri
        self.origin_airport = origin
        self.destination_airport = destination
        self.out_date = outday
        self.return_date = retday

def find_cheap(city, lowpr, flight):
        if flight is None or not flight['data']:
            return FlightData(city, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A')
        comp = []
        for blk in flight['data']:
            price = blk['price']['base']
            orig= blk['itineraries'][0]['segments'][0]['departure']['iataCode']
            dest = blk['itineraries'][0]['segments'][0]['arrival']['iataCode']
            out = blk['itineraries'][0]['segments'][0]['departure']['at']
            ret = blk['itineraries'][1]['segments'][0]['arrival']['at']

            so = FlightData(city, price, orig, dest, out, ret)
            comp.append(so)

        lowest = lowpr

        cheapest = None
        for blk2 in comp:
            if float(blk2.price) < float(lowest):
                lowest = blk2.price
                cheapest = blk2
        if cheapest is None:
            return FlightData(city, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A')
        else:
            return cheapest
