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
from __future__ import annotations
from typing import List, Tuple, Dict, Optional
from flight import Trip

"""
    FF_Status: Dict[str, Tuple(int, int)] where the Tuple(status miles to reach, 
               discount for fares from the next trip (NOT flight segment) after 
               the status is achieved). The units are (Kilometres, Percent).
"""
FREQUENT_FLYER_STATUS = {"Prestige": (15000, -10), "Elite-Light": (30000, -15),
                         "Elite-Regular": (50000, -20),
                         "Super-Elite": (100000, -25)}

"""
    FREQUENT_FLYER_MULTIPLIER: the key is the type of cabin class (seat type), 
                               the value is the miles multiplier (status miles 
                               are calculated by multiplying the flight length 
                               by this miles multiplier).
"""
FREQUENT_FLYER_MULTIPLIER = {"Economy": 1, "Business": 5}

"""
    CLASS_MULTIPLIER: used (with the FlightSegment's base cost to determine the 
                      actual cost of the segment based on the class of flight: 
                      Tuple(int, int)] taken by the customer, where the 
                      Tuple(class, multiplier).
"""
CLASS_MULTIPLIER = {"Economy": 1, "Business": 2.5}


class Customer:
    """ A Customer of Python Air.

    === Public Attributes ===
    name:
        the customer's name (may include one or all:
        first, middle, and last).
    age:
        the customer's age.
    nationality:
        the customer's nationality (there are no dual citizens).
    all_flight_costs:
        the sum of all flight costs this customer has taken over
        the course of their existence.

    Representation Invariants:
        - trips are stored per customer forever.
        - miles/status are accumulated and never lost.
    """

    # === Private Attributes ===
    # _customer_id:
    #     this is a unique 6-digit customer identifier.
    # _ff_status:
    #     this is the customer's frequent flyer status.
    # _miles:
    #     this is the running tally of the customer's
    #     total qualifying miles for their status.
    # _trips:
    #     this stores the dictionary of Trips and their
    #     corresponding costs.

    name: str
    age: int
    nationality: str
    all_flight_costs: float
    _customer_id: int
    _trips: Dict[Trip, float]
    _ff_status: str
    _miles: int

    def __init__(self, cus_id: int, name: str, age: int, nat: str) -> None:
        """ A Customer of Python Air. """

        self.name = name
        self.age = age
        self.nationality = nat
        self._customer_id = cus_id

        self.all_flight_costs = 0.0
        self._trips = {}
        self._ff_status = ""
        self._miles = 0

    def get_id(self) -> int:
        """ Returns this customer's identification (ID). """

        return self._customer_id

    def get_trips(self) -> List[Trip]:
        """ Returns a list of Trips booked for this customer. """

        return list(self._trips.keys())

    def get_total_flight_costs(self) -> float:
        """ Returns this customer's total flight costs. """

        return self.all_flight_costs

    def get_cost_of_trip(self, trip_lookup: Trip) -> Optional[float]:
        """ Returns the cost of that Trip, otherwise None.
        """

        if trip_lookup in self._trips:
            return self._trips[trip_lookup]

    def get_ff_status(self) -> str:
        """ Returns this customer's frequent flyer status. """

        return self._ff_status

    def get_miles(self) -> int:
        """ Returns this customer's qualifying miles. """

        return self._miles

    def book_trip(self, reservation_id: str,
                  segments: List[Tuple[FlightSegment, str]],
                  trip_date: datetime.date) -> Trip:
        """ Books the customer's trip and returns a Trip.

            <segments> are a List of Tuples, containing a (FlightSegment,
            seat_type) pair.

            Precondition: the customer is guaranteed to have a seat on each of
                          the <segments>.
        """
        all_flight_segments = []

        for each in segments:
            all_flight_segments.append(each[0])
            each[0].book_seat(self._customer_id, each[1])
            self._miles += each[0].get_length() * FREQUENT_FLYER_MULTIPLIER[
                each[1]]

        trip = Trip(reservation_id, self._customer_id, trip_date,
                    all_flight_segments)

        total_cost = 0
        for flight_segment in trip.get_flight_segments():
            seat_class = flight_segment.check_seat_class(self.get_id())
            cost_segment = flight_segment.get_base_fare_cost()
            cost_segment = cost_segment * CLASS_MULTIPLIER[seat_class]
            cost_segment = cost_segment * flight_segment.get_length()
            total_cost += cost_segment

        if self.get_ff_status() != "":
            total_cost = ((100 + FREQUENT_FLYER_STATUS[
                self.get_ff_status()][1]) / 100) * total_cost

        for each in FREQUENT_FLYER_STATUS:
            if self._miles >= FREQUENT_FLYER_STATUS[each][0]:
                self._ff_status = each

        self._trips[trip] = total_cost

        return trip

    def cancel_trip(self, canceled_trip: Trip,
                    segments: List[Tuple[FlightSegment, str]]) -> None:
        """ Cancels this customer's Trip.

            <segments> are a List of Tuples, containing the (FlightSegment,
            seat_type) pair.

            Precondition: the <canceled_trip> must be a valid Trip that this
                          customer has booked.
        """
        del self._trips[canceled_trip]

        for flight in segments:
            flight[0].cancel_seat(self._customer_id)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta',
            'typing',
            'doctest',
            'flight',
            '__future__',
        ],
        'max-attributes': 8,
    })
