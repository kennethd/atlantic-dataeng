
import csv
import datetime

from atldata.db import IntegerField, StringField, StateField, ValidationError


def ingest_file(filepath):

    with open(filepath, 'r') as fh:
        # iterate over records as lazy generator
        data = csv.reader(fh, delimiter='\t')
        for line in data:
            # there are nicer ways to do this
            assert len(line) == 11

            # customers table
            customer_id = line[0]
            first_name = line[1]
            last_name = line[2]
            address = line[3]
            state = line[4]
            zip_code = line[5]

            # products table
            product_id = line[7]
            product_name = line[8]

            # transaction table
            action = line[6]
            total = line[9]
            dt = line[10]

    return [
        'message one',
        'message two',
    ]

