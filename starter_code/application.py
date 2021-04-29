"""
UTM:CSC148, Winter 2020
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Bogdan Simion, Michael Liut, Paul Vrbik
"""
import datetime
import csv
from typing import Dict, List, Tuple, Optional
from airport import Airport
from customer import Customer
from flight import Trip, FlightSegment
from visualizer import Visualizer

#############################################
# DO NOT DECLARE ANY OTHER GLOBAL VARIABLES!
#############################################

# AIRPORT_LOCATIONS: global mapping of an airport's IATA with their respective
#                    longitude and latitude positions.
# NOTE: This is used for our testing purposes, so it has to be populated in
# create_airports(), but you are welcome to use it as you see fit.
AIRPORT_LOCATIONS = {}

# DEFAULT_BASE_COST: Default rate per km for the base cost of a flight segment.
DEFAULT_BASE_COST = 0.1225


def import_data(file_airports: str, file_customers: str, file_segments: str,
                file_trips: str) -> Tuple[List[List[str]], List[List[str]],
                                          List[List[str]], List[List[str]]]:
    """ Opens all the data files <data/filename.csv> which stores the CSV data,
        and returns a tuple of lists of lists of strings. This contains the read
        in data, line-by-line, (airports, customers, flights, trips).

        Precondition: the dataset file must be in CSV format.
    """

    airport_log, customer_log, flight_log, trip_log = [], [], [], []

    airport_data = csv.reader(open(file_airports))
    customer_data = csv.reader(open(file_customers))
    flight_data = csv.reader(open(file_segments))
    trip_data = csv.reader(open(file_trips))

    for row in airport_data:
        airport_log.append(row)

    for row in flight_data:
        flight_log.append(row)

    for row in customer_data:
        customer_log.append(row)

    for row in trip_data:
        trip_log.append(row)

    return airport_log, flight_log, customer_log, trip_log


def create_customers(log: List[List[str]]) -> Dict[int, Customer]:
    """ Returns a dictionary of Customer IDs and their Customer instances, based
    on the customers from the input dataset from the <log>.

    Precondition:
        - The <log> list contains the input data in the correct format.
    """
    id_customers = {}
    for customer in log:
        x = Customer(int(customer[0]), customer[1],
                     int(customer[2]), customer[3])
        id_customers[x.get_id()] = x
    return id_customers


def create_flight_segments(log: List[List[str]])\
        -> Dict[datetime.date, List[FlightSegment]]:
    """ Returns a dictionary storing all FlightSegments, indexed by their
    departure date, based on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    """

    flight_segments = {}
    for each in log:
        date = each[3].split(":")
        dep_time = each[4].split(":")
        arr_time = each[5].split(":")

        dep = datetime.datetime(int(date[0]), int(date[1]), int(date[2]),
                                int(dep_time[0]), int(dep_time[1]))
        arr = datetime.datetime(int(date[0]), int(date[1]), int(date[2]),
                                int(arr_time[0]), int(arr_time[1]))
        if dep > arr:
            arr += datetime.timedelta(days=1)

        dep_loc = AIRPORT_LOCATIONS[each[1]]
        arr_loc = AIRPORT_LOCATIONS[each[2]]
        x = FlightSegment(each[0], dep, arr, DEFAULT_BASE_COST, float(each[6]),
                          each[1], each[2], (dep_loc, arr_loc))
        y = datetime.date(x.get_times()[0].year, x.get_times()[0].month,
                          x.get_times()[0].day)
        if y in flight_segments:
            flight_segments[y].append(x)
        else:
            flight_segments[y] = [x]
    return flight_segments


def create_airports(log: List[List[str]]) -> List[Airport]:
    """ Return a list of Airports with all applicable data, based
    on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    """

    all_airports = []
    for each in log:
        all_airports.append(Airport(each[0], each[1],
                                    (float(each[2]), float(each[3]))))
        AIRPORT_LOCATIONS[each[0]] = (float(each[2]), float(each[3]))
    return all_airports


def load_trips(log: List[List[str]], customer_dict: Dict[int, Customer],
               flight_segments: Dict[datetime.date, List[FlightSegment]]) \
        -> List[Trip]:
    """ Creates the Trip objects and makes the bookings.

    Preconditions:
    - The <log> list contains the input data in the correct format.
    - the customers are already correctly stored in the <customer_dict>,
    indexed by their customer ID.
    - the flight segments are already correctly stored in the <flight_segments>,
    indexed by their departure date
    """
    all_trips = []
    for each in log:
        z = []

        for flight in each[3:]:
            flight = flight.strip("[").strip("(").strip("]")
            flight = flight.strip(")").strip("'").strip('"')
            z.append(str(flight))

        for i in range(0, len(z), 2):
            z[i] = (z[i], z[i+1])

        z = z[::2]

        curr_date_time = each[2].split("-")

        trip_date = datetime.date(int(curr_date_time[0]),
                                  int(curr_date_time[1]),
                                  int(curr_date_time[2]))

        curr_date_time = datetime.datetime(int(curr_date_time[0]),
                                           int(curr_date_time[1]),
                                           int(curr_date_time[2]), 0, 0)

        trip_works = True

        index_trip = 0

        all_flight_segments = []

        while index_trip < len(z)-1:

            if each[0] == "None":
                trip_works = False
                break

            current_index_trip = index_trip

            date = datetime.date(curr_date_time.year, curr_date_time.month,
                                 curr_date_time.day)

            if date == max(flight_segments)+datetime.timedelta(days=1):
                trip_works = False
                break

            if flight_segments[date] is not None:
                for flight in flight_segments[date]:
                    if flight.get_times()[0] >= curr_date_time and \
                            flight.seat_availability[z[index_trip][1]] > 0 and \
                            flight.get_dep() == z[index_trip][0] and \
                            flight.get_arr() == z[index_trip+1][0]:

                        index_trip += 1
                        all_flight_segments.append((flight, z[index_trip-1][1]))
                        curr_date_time = flight.get_times()[1]
                        break

            if current_index_trip == index_trip:
                curr_date_time = datetime.datetime(curr_date_time.year,
                                                   curr_date_time.month,
                                                   curr_date_time.day, 0, 0, 0)
                curr_date_time += datetime.timedelta(days=1)

        if trip_works:
            all_trips.append(customer_dict[int(each[1])].book_trip(
                str(each[0]), all_flight_segments, trip_date))

    return all_trips


if __name__ == '__main__':
    print("\n---------------------------------------------")
    print("Reading in all data! Processing...")
    print("---------------------------------------------\n")

    #input_data = import_data('data/airports.csv', 'data/customers.csv',
    #                         'data/segments.csv', 'data/trips.csv')
    input_data = import_data('data/airports.csv', 'data/customers.csv',
                           'data/segments_small.csv', 'data/trips_small.csv')

    airports = create_airports(input_data[0])
    print("Airports Created! Still Processing...")
    flights = create_flight_segments(input_data[1])
    print("Flight Segments Created! Still Processing...")
    customers = create_customers(input_data[2])
    print("Customers Created! Still Processing...")
    print("Loading trips can take a while...")
    trips = load_trips(input_data[3], customers, flights)
    print("Trips Created! Opening Visualizer...\n")

    flights_len = 0
    for ky in flights:
        flights_len += len(flights[ky])

    print("---------------------------------------------")
    print("Some Statistics:")
    print("---------------------------------------------")
    print("Total airports in the dataset:", len(airports))
    print("Total flight segments in the dataset:", flights_len)
    print("Total customers in the dataset:", len(customers))
    print("Total trips in the dataset:", len(trips))
    print("---------------------------------------------\n")

    all_flights = [seg for tp in trips for seg in tp.get_flight_segments()]
    all_customers = [customers[cid] for cid in customers]

    V = Visualizer()
    V.draw(all_flights)

    while not V.has_quit():

        flights = V.handle_window_events(all_customers, all_flights)

        all_flights = []

        for flt in flights:
            all_flights.append(flt)

        V.draw(all_flights)

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'csv', 'datetime', 'doctest',
            'visualizer', 'customer', 'flight', 'airport'
        ],
        'max-nested-blocks': 6,
        'allowed-io': [
            'create_customers', 'create_airports', 'import_data',
            'create_flight_segments', 'load_trips'
        ],
        'generated-members': 'pygame.*'
    })
