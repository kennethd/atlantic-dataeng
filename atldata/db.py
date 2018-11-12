
import sqlite3


US_STATES = [
    'AK', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
    'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
]


class ValidationError(Exception):
    pass


class DbField(object):

    def __init__(self, colname, value, maxlength=0, required=False):
        self.colname = colname
        self.value = value
        self.required = required
        self.maxlength = maxlength

    def err(msg):
        msg = '{}: {}'.format(self.colname, msg)
        raise ValidationError(msg)

    def validate(self):
        if not colname:
            self.err('colname not set')

        if self.required and not self.value:
            self.err('Required value')

        if self.maxlength and len(self.value) > self.maxlength:
            self.err('Truncated Value!  {}'.format(self.value[:self.maxlength]))


class IntegerField(DbField):
    def validate(self):
        super(IntegerField, self).validate()
        if not isinstance(self.value, int):
            self.err('Need an integer, got {}:{}'.format(type(self.value), self.value))


class StringField(DbField):
    def validate(self):
        super(StringField, self).validate()
        if not isinstance(self.value, basestring):
            self.err('Need an string, got {}:{}'.format(type(self.value), self.value))


class StateField(StringField):
    def __init__(self, colname, value, maxlength=0, required=False):
        super(StateField, self).__init__(colname, value, maxlength=2, required=required)

    def validate(self):
        super(StateField, self).validate()
        if not self.value.upper() in US_STATES:
            self.err('Unrecognized State: {}'.format(self.value.upper()))


class DateTimeField(StringField):

    def validate(self):
        super(DateTimeField, self).validate()
        # try/except parsing isoformat


class DbTable(object):
    def validate(self):
        for colname, field in self.columns:
            field.validate()

    def save(self):
        # All-or-nothing, raises ValidationError or doesn't
        self.validate()


class Customer(DbTable):
    table_name = 'customers'

    def __init__(self, id=None, first_name=None, last_name=None, address=None, state=None, zip_code=None):
        self.columns = {
            'id': IntegerField('id', id),
            'first_name': StringField('first_name', first_name, required=True),
            'last_name': StringField('last_name', last_name, required=True),
            'address': StringField('address', address),
            'state': StateField('state', state),
            'zip': StringField('zip', zip_code),
        }


class Product(DbTable):
    table_name = 'products'

    def __init__(self, id=None, name=None, price=None):
        self.columns = {
            'id': IntegerField('id', id),
            'name': StringField('name', name, maxlength=100, required=True),
            'price': IntegerField('price', price, required=True),
        }


class Transaction(DbField):
    table_name = 'transactions'

    def __init__(self, id=None, customer_id=None, product_id=None, dt=None):
        self.columns = {
            'id': IntegerField('id', id),
            'customer_id': IntegerField('customer_id', customer_id, required=True),
            'product_id': IntegerField('product_id', product_id, required=True),
        }



