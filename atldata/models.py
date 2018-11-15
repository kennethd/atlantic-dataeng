
import logging

from atldata.db import dbconn, upsert


log = logging.getLogger(__name__)


US_STATES = [
    'AK', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
    'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
]


class ValidationError(ValueError):
    pass

class DataWarning(UserWarning):
    pass


class DbField(object):

    def __init__(self, colname, value, maxlength=0, required=False):
        self.colname = colname
        self.value = value
        self.required = required
        self.maxlength = maxlength

    def err(self, msg):
        msg = '{}: {}'.format(self.colname, msg)
        raise ValidationError(msg)

    def validate(self):
        if not self.colname:
            self.err('colname not set')

        if self.required and not self.value:
            self.err('Required value')

        if self.maxlength and len(self.value) > self.maxlength:
            self.err('Truncated Value!  {}'.format(self.value[:self.maxlength]))


class IntegerField(DbField):
    def validate(self):
        super(IntegerField, self).validate()
        try:
            self.value = int(self.value)
        except ValueError:
            msg = 'Need an integer, got {}:{}'.format(type(self.value), self.value)
            self.err(msg)


class StringField(DbField):
    def validate(self):
        super(StringField, self).validate()
        try:
            self.value = self.value.strip()
        except AttributeError:
            msg = 'Need a string, got {}:{}'.format(type(self.value), self.value)
            self.err(msg)


class StateField(StringField):
    def __init__(self, colname, value, maxlength=0, required=False):
        # force maxlength = 2
        super(StateField, self).__init__(colname, value, maxlength=2, required=required)

    def validate(self):
        super(StateField, self).validate()
        if not self.value.upper() in US_STATES:
            self.err('Unrecognized State: {}'.format(self.value.upper()))


class CurrencyField(IntegerField):
    def __init__(self, colname, value, maxlength=0, required=False):
        # force currency to be stored as cents
        try:
            value = value.replace('.', '')
        except AttributeError:
            pass
        super(CurrencyField, self).__init__(colname, value, maxlength=maxlength, required=required)

class DateTimeField(StringField):

    def validate(self):
        super(DateTimeField, self).validate()
        # TODO: try/except parsing isoformat


class DbTable(object):
    table_name = None
    pk = None

    def validate(self):
        for col in self.columns:
            col.validate()

    def colvals(self):
        "returns tuple of 2 lists (colnames, values)"
        colnames = []
        values = []
        for c in self.columns:
            colnames.append(c.colname)
            values.append(c.value)
        return (colnames, values)

    def save(self, cur):
        # All-or-nothing, raises ValidationError or doesn't
        self.validate()
        colnames, values = self.colvals()

        where = {}
        print("save(): PK:{} COLNAMES:{}".format(self.pk, colnames))
        if self.pk and colnames.index(self.pk) > -1:
            where = {self.pk: values[colnames.index(self.pk)]}

        count = upsert(cur, self.table_name, colnames, values, where)

        return count


class Customer(DbTable):
    table_name = 'customers'
    pk = 'id'

    def __init__(self, id=None, first_name=None, last_name=None, address=None, state=None, zip_code=None):
        self.columns = {
            IntegerField('id', id),
            StringField('first_name', first_name, required=True),
            StringField('last_name', last_name, required=True),
            StringField('address', address),
            StateField('state', state),
            StringField('zip', zip_code),
        }


class Product(DbTable):
    table_name = 'products'
    pk = 'id'

    def __init__(self, id=None, name=None):
        self.columns = {
            IntegerField('id', id),
            StringField('name', name, maxlength=100, required=True),
        }


class Transaction(DbTable):
    table_name = 'transactions'

    def __init__(self, customer_id, product_id, action=None, amount=None, dt=None):
        self.customer_id = customer_id
        self.product_id = product_id
        self.action = action

        self.columns = {
            IntegerField('customer_id', customer_id, required=True),
            IntegerField('product_id', product_id, required=True),
            StringField('action', action, required=True),
            CurrencyField('amount', amount),
            DateTimeField('dt', 'dt', required=True),
        }

    def save(self, cur):
        super(Transaction, self).save(cur)

        # in addition to recording transaction log, this model also maintains
        # the current status of each customer<->product relationship via a
        # UNIQUE constraint on the customers_products table's (customer_id,
        # product_id) columns.
        cols = ['customer_id', 'product_id', 'status']
        vals = [self.customer_id, self.product_id, self.action]
        where = {'customer_id': self.customer_id, 'product_id': self.product_id}
        count = upsert(cur, 'customers_products', cols, vals, where)
        if not count:
            log.warn('Failed to upsert customers_products')

