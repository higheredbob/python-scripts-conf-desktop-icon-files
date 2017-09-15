#!/usr/bin/python

import datetime
import sqlite3 as sql
import argparse
import sys

parser = argparse.ArgumentParser(description="parse a dir cont. sqlite files")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase the output of information")
parser.add_argument("-f", "--filename", nargs="?", dest='database', 
                    default=sys.stdin,
                    help="input a dbfile to process")
args = parser.parse_args()

def fixDate(timestamp):
    #Chrome stores timestamps in the number of microseconds since Jan 1 1601.
    #To convert, we create a datetime object for Jan 1 1601...
    epoch_start = datetime.datetime(1601,1,1)
    #create an object for the number of microseconds in the timestamp
    delta = datetime.timedelta(microseconds=int(timestamp))
    #and return the sum of the two.
    return epoch_start + delta

selectStatement = "SELECT id, baseDomain, name, expiry, lastAccessed, creationTime FROM moz_cookies"
db = args.database #args.filename()
con = sql.connect(db)
c = con.cursor()
for row in c.execute(selectStatement):
    print "id:",str(row[0])
    print "\tdomain:",str(row[1])
    print "\tname:",str(row[2])
    print "\texpires:",str(fixDate(row[3]))
    print "\tlast_accessed:",str(fixDate(row[4]))
    print "\tcreate_date:",str(fixDate(row[5]))