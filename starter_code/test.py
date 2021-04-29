from application import import_data
from application import create_flight
import datetime

if __name__ == '__main__':

    input_data = import_data('data/airports.csv', 'data/customers.csv',
                             'data/segments_small.csv', 'data/trips_small.csv')
    x = input_data[3][0][3:]
    y = []
    z = []

    for each in x:
        each = each.strip("[").strip("(").strip("]")
        each = each.strip(")").strip("'").strip('"')
        y.append(str(each))

    for i in range(0, len(y), 2):
        z.append((y[i], y[i+1]))
