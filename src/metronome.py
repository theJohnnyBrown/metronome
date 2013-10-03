#! /usr/bin/env python

import os
from datetime import datetime
import urlparse

import psycopg2

DB_CONN = os.environ['METRONOME_DB']

def clock_in(**kwargs):
    kwargs['time_in'] = datetime.utcnow() if not kwargs.get("time_in") else when

    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(DB_CONN)

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)

    cur = conn.cursor()

    vals = filter(None, kwargs.items())

    query = ("INSERT INTO entries (" + ", ".join([v[0] for v in vals]) + ")" +
             " VALUES (" + ", ".join(["%s" for v in vals]) + ")")
    cur.execute(query, tuple(v[1] for v in vals))
    conn.commit()
