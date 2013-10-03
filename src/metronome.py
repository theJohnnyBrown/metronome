#! /usr/bin/env python

import os
from datetime import datetime

import psycopg2

DB_CONN = os.environ['METRONOME_DB']

def clock_in(**kwargs):
    when = datetime.utcnow() if not kwargs.get("time_in") else when

    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    vals = filter(None, kwargs.items())

    query = ("INSERT INTO entries (" + ", ".join([v[0] for v in vals]) + ")" +
             " VALUES (" + ", ".join(["%s" for v in vals]) + ")")
    cur.execute(query, tuple(v[1] for v in vals))
    
