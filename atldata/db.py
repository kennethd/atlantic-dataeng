
import sqlite3


def create_db(cur, schema):
    """reads schema file from disk & creates db"""

def connection(connstr):
    """connstr may be ':memory:' or path to file, yields cursor"""

    try:
        conn = sqlite3.connect(dbfile)
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_keys = ON;')
        yield cur
    except sqlite3.OperationalError as ex:
        raise
    else:
        conn.close

