#! /usr/bin/env python

import os
from datetime import datetime, timedelta
import urlparse
import psycopg2

from exporters.standard import export as se


urlparse.uses_netloc.append("postgres")
DB_CONN = os.environ['METRONOME_DB']

def clock_in(**kwargs):
    kwargs['time_in'] = datetime.utcnow() if not kwargs.get("time_in") else kwargs["time_in"]

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

def clock_out(**kwargs):
    kwargs['time_out'] = datetime.utcnow() if not kwargs.get("time_out") else kwargs["time_out"]

    url = urlparse.urlparse(DB_CONN)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
    cur = conn.cursor()

    vals = filter(None, kwargs.items())

    latest_query = "SELECT id FROM entries order by time_in desc"
    cur.execute(latest_query)
    latest_id = cur.fetchone()[0]

    query = ("UPDATE entries SET " +
             ", ".join([k + "=%s" for k, v in vals])
             + " where id=%s")
    cur.execute(query, list(v[1] for v in vals) + [str(latest_id)])
    conn.commit()