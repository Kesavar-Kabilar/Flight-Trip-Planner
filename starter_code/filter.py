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
from typing import List
from customer import Customer
from flight import FlightSegment
# from time import sleep


class Filter:
    """ A class for filtering flight segments based on some criterion.

        This is an abstract class. Only subclasses should be instantiated.
    """
    def __init__(self) -> None:
        pass

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data>, which match the
            filter specified in <filter_string>.

            The <filter_string> is provided by the user through the visual
            prompt, after selecting this filter.

            The <customers> is a list of all customers from the input dataset.

            If the filter has no effect or the <filter_string> is invalid then
            return the same flights segments from the <data> input.

            Precondition:
                - <customers> contains the list of all customers from the input
                  dataset
                - all flight segments included in <data> are valid segments
                  from the input dataset
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu
        """
        raise NotImplementedError


class ResetFilter(Filter):
    """ A class for resetting all previously applied filters, if any. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Reset all of the applied filters. Returns a List containing all the
            flight segments corresponding to all trips of <customers>.

            The <data>, <customers>, and <filter_string> arguments for this
            type of filter are ignored.
        """
        print(len(data))
        data = [seg for customer in customers
                for trip in customer.get_trips()
                for seg in trip.get_flight_segments()]
        print(len(data))

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Reset all of the filters applied so far (if any)!"


class CustomerFilter(Filter):
    """ A class for selecting the flight segments for a given customer. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> made or received
            by the customer with the id specified in <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            customer ID.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        filter_customer = ""

        for customer in customers:
            if customer.get_id() == int(filter_string):
                filter_customer = customer

        if filter_customer != "":
            customer_flight_segments = []
            for trip in filter_customer.get_trips():
                for flight_segment in trip.get_flight_segments():
                    if flight_segment in data:
                        customer_flight_segments.append(flight_segment)
            for i in range(len(data)-1, -1, -1):
                if data[i] not in customer_flight_segments:
                    data.pop(i)

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter events based on customer ID"


class DurationFilter(Filter):
    """ A class for selecting only the flight segments lasting either over or
        under a specified duration.
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> with a duration of
            under or over the time indicated in the <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains the following
            input format: either "Lxxxx" or "Gxxxx", indicating to filter
            flight segments less than xxxx or greater than xxxx minutes,
            respectively.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        if len(filter_string) > 1 and filter_string[0] == 'L' and \
                filter_string[1:].isnumeric():
            duration = int(filter_string[1:])
            for i in range(len(data)-1, -1, -1):
                flight_duration = data[i].get_duration().hour * 60
                flight_duration += data[i].get_duration().minute

                if flight_duration >= duration:
                    data.pop(i)

        elif len(filter_string) > 1 and filter_string[0] == 'G' and \
                filter_string[1:].isnumeric():
            duration = int(filter_string[1:])
            for i in range(len(data)-1, -1, -1):
                flight_duration = data[i].get_duration().hour*60
                flight_duration += data[i].get_duration().minute

                if flight_duration <= duration:
                    data.pop(i)

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu
        """
        return "Filter flight segments based on duration; " \
               "L#### returns flight segments less than specified length, " \
               "G#### for greater "


class LocationFilter(Filter):
    """ A class for selecting only the flight segments which took place within
        a specific area.
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data>, which took place
            within a location specified by the <filter_string> (the IATA
            departure or arrival airport code of the segment was
            <filter_string>).

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            3-string IATA airport code. In the event of an invalid string:
              1. return the original list <data>, and
              2. your code must not crash.
        """
        if len(filter_string) == 4 and filter_string.isupper() and \
                filter_string.isalpha() and filter_string[0] == "D":
            for i in range(len(data)-1, -1, -1):
                if not data[i].get_dep() == filter_string[1:]:
                    data.pop(i)
        elif len(filter_string) == 4 and filter_string.isupper() and \
                filter_string.isalpha() and filter_string[0] == "A":
            for i in range(len(data)-1, -1, -1):
                if not data[i].get_arr() == filter_string[1:]:
                    data.pop(i)

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter flight segments based on an airport location;\n" \
               "DXXX returns flight segments that depart airport XXX,\n"\
               "AXXX returns flight segments that arrive at airport XXX\n"


class DateFilter(Filter):
    """ A class for selecting all flight segments that departed and arrive
    between two dates (i.e. "YYYY-MM-DD/YYYY-MM-DD" or "YYYY MM DD YYYY MM DD").
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> that have departed
            and arrived between the range of two dates indicated in the
            <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains the following
            input format: either "YYYY-MM-DD/YYYY-MM-DD" or
            "YYYY MM DD YYYY MM DD", indicating to filter flight segments
            between the first occurrence of YYYY-MM-DD and the second occurence
            of YYYY-MM-DD.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        if len(filter_string) == 21:

            if filter_string[4:5] == "-":

                a = filter_string[0:4].isnumeric() and filter_string[4:5] == "-"
                b = filter_string[5:7].isnumeric() and filter_string[7:8] == "-"
                c = filter_string[8:10].isnumeric() and \
                    filter_string[10:11] == "/"
                d = filter_string[11:15].isnumeric() and \
                    filter_string[15:16] == "-"
                e = filter_string[16:18].isnumeric() and \
                    filter_string[18:19] == "-"
                f = filter_string[19:21].isnumeric()

                if a and b and c and d and e and f:

                    start = datetime.datetime(int(filter_string[0:4]),
                                              int(filter_string[5:7]),
                                              int(filter_string[8:10]), 0, 0)

                    end = datetime.datetime(int(filter_string[11:15]),
                                            int(filter_string[16:18]),
                                            int(filter_string[19:21]), 23, 59)

                    for i in range(len(data)-1, -1, -1):
                        flight_time = data[i].get_times()

                        if not (start <= flight_time[0] <= end and
                                start <= flight_time[1] <= end):
                            data.pop(i)

            elif filter_string[4:5] == " ":

                a = filter_string[0:4].isnumeric() and filter_string[4:5] == " "
                b = filter_string[5:7].isnumeric() and filter_string[7:8] == " "
                c = filter_string[8:10].isnumeric() and \
                    filter_string[10:11] == " "
                d = filter_string[11:15].isnumeric() and \
                    filter_string[15:16] == " "
                e = filter_string[16:18].isnumeric() and \
                    filter_string[18:19] == " "
                f = filter_string[19:21].isnumeric()

                if a and b and c and d and e and f:

                    start = datetime.datetime(int(filter_string[0:4]),
                                              int(filter_string[5:7]),
                                              int(filter_string[8:10]), 0, 0)

                    end = datetime.datetime(int(filter_string[11:15]),
                                            int(filter_string[16:18]),
                                            int(filter_string[19:21]), 23, 59)

                    for i in range(len(data)-1, -1, -1):
                        flight_time = data[i].get_times()

                        if not (start <= flight_time[0] <= end and
                                start <= flight_time[1] <= end):
                            data.pop(i)
        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter flight segments based on dates; " \
               "'YYYY-MM-DD/YYYY-MM-DD' or 'YYYY-MM-DD,YYYY-MM-DD'"


class TripFilter(Filter):
    """ A class for selecting the flight segments for a trip. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> where the
            <filter_string> specified the trip's reservation id.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            Reservation ID.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        data = []
        for customer in customers:
            if customer.get_trips() is not None:
                for trip in customer.get_trips():
                    if trip.get_reservation_id() == filter_string:
                        data.extend(trip.get_flight_segments())

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter events based on a reservation ID"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'doctest',
            'customer', 'flight', 'time'
        ],
        'max-nested-blocks': 5,
        'allowed-io': ['apply', '__str__']
    })
