#! /usr/bin/env python
import os
import psycopg2
import urlparse

DB_CONN = os.environ['METRONOME_DB']

def export(where=None):
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(DB_CONN)

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
    cur = conn.cursor()

    if where:
        query = ("SELECT time_in, time_out, client, notes FROM entries WHERE " +
                 where +
                 " order by time_in desc")
    else:
        query = ("SELECT time_in, time_out, client, notes FROM entries"
                 " order by time_in desc")
    cur.execute(query)
    records = []
    for e in cur.fetchall():
        time_in, time_out, client, notes = e
        records.append({"time_in": time_in, "time_out": time_out,
                       "client": client, "notes": notes})
    return records