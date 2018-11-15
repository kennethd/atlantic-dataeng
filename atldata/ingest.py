
import csv
import datetime

from atldata.models import Customer, Product, Transaction, ValidationError, DataWarning


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
    amount = line[9]
    dt = line[10]

    # .validate() may raise ValidationError, subclass of ValueError
    cust = Customer(customer_id, first_name, last_name, address, state, zip_code)
    cust.validate()
    prod = Product(product_id, product_name)
    prod.validate()
    trans = Transaction(customer_id, product_id, action, amount, dt)
    trans.validate()

    # ok to insert/update


def ingest_file(filepath):
    status = {'success': 0, 'errors': [], 'warnings': []}
    with open(filepath, 'r') as fh:
        # iterate over records as lazy generator
        data = csv.reader(fh, delimiter='\t')
        for line in data:
            try:
                line_data = line_parser(line)
            except ValidationError as ex:
                status['errors'].append('RECORD PARSE ERROR: {}'.format(ex))
            except DataWarning as ex:
                status['warnings'].append('Warning: {}'.format(ex))

    status['warnings'].append('Test Warning')
    status['errors'].append('Test Error One')
    status['errors'].append('Test Error Two')
    return status

