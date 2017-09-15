#!/usr/bin/env python

"""outfile is utilized here, dumps an sqlite db, into an csv. This file can work on
some corrupt databases
"""

import argparse
import sqlite3 as sql
import csv
import sys
import datetime

usage = "parse a cache file in google chrome cache"
parser = argparse.ArgumentParser(usage=usage)

parser.add_argument("-f", "--filename", nargs="?", dest='database',
                    default=sys.stdin,
                    help="input a dbfile to process")
parser.add_argument('-o', '--outfile', default=sys.stdout,
                    nargs="?", dest='outfile', action='store',
                    help="file to write, default to stdout")

args = parser.parse_args()

def fixDate(timestamp):
    #Chrome stores timestamps in the number of microseconds since Jan 1 1601.
    #To convert, we create a datetime object for Jan 1 1601...
    epoch_start = datetime.datetime(1601,1,1)
    #create an object for the number of microseconds in the timestamp
    delta = datetime.timedelta(microseconds=int(timestamp))
    #and return the sum of the two.
    return epoch_start + delta

if args.database == None:
    print "unable to connect to a db" + usage
    exit(1)

selectStatement = "SELECT key, value FROM ItemTable"
db = args.database #args.filename()
con = sql.connect(db)
c = con.cursor()
for row in c.execute(selectStatement):
    print "key:",row[0].encode('utf-8')
    print "\tvalue:",str(row[1])
    if args.outfile != '':
        with open(args.outfile, 'w') as myfile:
            tablerows = c.fetchall()
            for tablerow in tablerows:
                writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                writer.writerow(tablerow)
