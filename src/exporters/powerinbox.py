#! /usr/bin/env python
import os
import psycopg2
import urlparse

DB_CONN = os.environ['METRONOME_DB']

def export():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(DB_CONN)

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
    cur = conn.cursor()

    query = "SELECT time_in, time_out, notes FROM entries WHERE client='powerinbox' order by time_in desc"
    cur.execute(query)
    for e in cur.fetchall():
        time_in, time_out, notes = e

        print "\t".join([time_in.strftime("%Y-%m-%d"),
                         str((time_out - time_in).total_seconds()/3600.0) if time_out else "",
                         notes if notes else "",
                         "", # "Sent to payroll field
                         str(time_in),
                         str(time_out) if time_out else ""])
