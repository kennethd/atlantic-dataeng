
import csv
import datetime

from atldata.db import IntegerField, StringField, StateField, ValidationError



def line_parser(line):

    if not len(line) == 11:
        raise ValueError('Unexpected number of columns ({}) for {}'.format(len(line), line))

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


def ingest_file(filepath):
    status = {'success': 0, 'errors': []}
    with open(filepath, 'r') as fh:
        # iterate over records as lazy generator
        data = csv.reader(fh, delimiter='\t')
        for line in data:
            try:
                line_data = line_parser(line)
            except ValueError as ex:
                status.errors(append('RECORD PARSE ERROR: {}'.format(ex)))
            except Exception as ex:
                status.errors(append('UNEXPECTED ERROR WHILE PARSING {}: {}'.format(line, ex)))
            else:
                status['success'] = status['success'] + 1

    status['errors'].append('Error One')
    status['errors'].append('Error Two')
    return status

