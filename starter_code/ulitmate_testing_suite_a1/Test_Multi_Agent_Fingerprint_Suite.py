from application import *
import hashlib
import flight
 
 
###
# SETUP INSTRUCTIONS:
# STEP 1: In Folder 'starter_code' > create a folder > ulitmate_testing_suite_a1 > Save this file underneath it as
# 'Test_Multi_Agent_Fingerprint_Suite.py'
# STEP 2: Add your tester name
###
def deep_fingerprint_trip_id():
    input_data_small = import_data('../data/airports.csv',
                                   '../data/customers.csv',
                                   '../data/segments_small.csv',
                                   '../data/trips_small.csv')
    input_data_big = import_data('../data/airports.csv',
                                 '../data/customers.csv',
                                 '../data/segments.csv', '../data/trips.csv')
    small_string = ''
    big_sting = ''
    airports = create_airports(input_data_small[0])
    customers = create_customers(input_data_small[2])
 
    flights_small = create_flight_segments(input_data_small[1])
    trips_small = load_trips(input_data_small[3], customers, flights_small)
 
    flights_big = create_flight_segments(input_data_big[1])
    trips_big = load_trips(input_data_big[3], customers, flights_big)
 
    for t in trips_small:
        small_string += t.get_reservation_id() + str(t.trip_departure) + f'{t.get_in_flight_time()}{t.get_in_flight_time()}{round(t.get_total_trip_time())}'
        for s in t.get_flight_segments():
            small_string += str(s.seat_availability)
            for element in s._manifest:
                small_string += str(element)
 
    for t in trips_big:
        big_sting += t.get_reservation_id() + str(t.trip_departure) + f'{t.get_in_flight_time()}{t.get_in_flight_time()}{round(t.get_total_trip_time())}'
        for s in t.get_flight_segments():
            big_sting += str(s.seat_availability)
            for element in s._manifest:
                big_sting += str(element)
    return small_string, big_sting
 
 
def deep_fingerprint_trip_id_limited():
    input_data_small = import_data('../data/airports.csv',
                                   '../data/customers.csv',
                                   '../data/segments_small.csv',
                                   '../data/trips_small.csv')
    input_data_big = import_data('../data/airports.csv',
                                 '../data/customers.csv',
                                 '../data/segments.csv', '../data/trips.csv')
    small_limited = ''
    big_limited = ''
    airports = create_airports(input_data_small[0])
    customers = create_customers(input_data_small[2])
 
    flight.AIRPLANE_CAPACITY = {"Economy": 2, "Business": 1}
    flights_small = create_flight_segments(input_data_small[1])
    trips_small = load_trips(input_data_small[3], customers, flights_small)
 
    flights_big = create_flight_segments(input_data_big[1])
    trips_big = load_trips(input_data_big[3], customers, flights_big)
 
    for t in trips_small:
        small_limited += t.get_reservation_id() + str(t.trip_departure) + f'{t.get_in_flight_time()}{t.get_in_flight_time()}{round(t.get_total_trip_time())}'
        for s in t.get_flight_segments():
            small_limited += str(s.seat_availability)
            for element in s._manifest:
                small_limited += str(element)
 
    for t in trips_big:
        big_limited += t.get_reservation_id() + str(t.trip_departure) + f'{t.get_in_flight_time()}{t.get_in_flight_time()}{round(t.get_total_trip_time())}'
        for s in t.get_flight_segments():
            big_limited += str(s.seat_availability)
            for element in s._manifest:
                big_limited += str(element)
 
    return small_limited, big_limited
 
 
if __name__ == "__main__":
    small, big = deep_fingerprint_trip_id()
    small_limited, big_limited = deep_fingerprint_trip_id_limited()
    print("Small MD5 Fingerprint : " + hashlib.md5(
        (small).encode('utf-8')).hexdigest())
    print("big MD5 Fingerprint : " + hashlib.md5(
        (big).encode('utf-8')).hexdigest())
    print("Small_limited MD5 Fingerprint : " + hashlib.md5(
        (small_limited).encode('utf-8')).hexdigest())
    print("big_limited MD5 Fingerprint : " + hashlib.md5(
        (big_limited).encode('utf-8')).hexdigest())
