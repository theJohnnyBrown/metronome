metronome
=========

An idiosyncratic time tracking library.

Examples
========

Clock in right now

    clock_in(client="Joe's burgers",
             project="New website")
    
Forgot to clock in? The `clock_in` function takes a `time_in` argument. Also `datetime.datetime` and `datetime.timedelta` are imported for you  by the `metronome` command.

    clock_in(client="globocorp", project='reporting tools',
             time_in=datetime.utcnow() - timedelta(hours=3))

Clock out right now

    clock_out(notes="Meeting with CTO")

`clock_out` also takes an argument to specify time

    clock_out(time_out=datetime.strptime('Fri Mar 14 23:54:11 2014', '%c'))
