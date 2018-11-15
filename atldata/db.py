
import contextlib
import logging
import os
import sqlite3


log = logging.getLogger(__name__)


def create_db(cur, schema_file):
    """reads schema file from disk & creates db"""
    with open(schema_file, 'rw') as fh:
        return cur.executescript(fh.read())


@contextlib.contextmanager
def dbconn(dbpath, schemapath):
    """dbpath may be ':memory:' or path to file, yields cursor"""
    print('opening db file {}'.format(dbpath))
    try:
        conn = sqlite3.connect(dbpath)
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_keys = ON;')
        objects = cur.execute('SELECT * FROM sqlite_master ;').fetchall()
        if not objects:
            log.warn('No db objects exist. creating db')
            res = create_db(cur, schemapath)
            log.info('create_db() returned {}'.format(res))
        yield cur
        conn.commit()
    except sqlite3.OperationalError as ex:
        log.error(ex)
        raise
    else:
        conn.close


def insert(cur, tablename, colnames, values):
    """colnames & values are lists with the corresponding name & value
    guaranteed to be at the same index position in each list.  returns count
    of rows inserted"""
    colstr = ', '.join(colnames)
    places = ', '.join(['?'] * len(values))
    sql = 'INSERT INTO {} ({}) VALUES ({})'.format(tablename, colstr, places)
    log.info(sql, values)
    cur.execute(sql, values)
    return cur.rowcount


def update(cur, tablename, colnames, values, where):
    """colnames & values are lists with the corresponding name & value
    guaranteed to be at the same index position in each list, where is a dict
    of column {name: value} pairs.  returns count of rows updated"""
    colstr = ', '.join([ '{} = ?'.format(c) for c in colnames ])
    wherecols = []
    wherevals = []
    for col, val in where.items():
        wherecols.append(col)
        wherevals.append(val)
    wherestr = ' AND '.join([ '{} = ?'.format(c) for c in wherecols ])
    sql = 'UPDATE {} SET {} WHERE {}'.format(tablename, colstr, wherestr)
    print(sql, values + wherevals)
    cur.execute(sql, values + wherevals)
    return cur.rowcount


def upsert(cur, tablename, colnames, values, where=None):
    """super-simple upsert emulation"""
    print('UPSERT {}:{} VALUES:{} WHERE:{}'.format(tablename, colnames, values, where))
    count = 0
    if where:
        count = update(cur, tablename, colnames, values, where)
    if not count:
        count = insert(cur, tablename, colnames, values)
    return count

