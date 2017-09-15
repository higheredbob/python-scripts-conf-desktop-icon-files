#!/usr/bin/env python

import sqlite3 as sql
import argparse
import sys
import datetime




usage = "\nConnect to a cookies db, enumerate table and rows, export that info to stdout or file \n\
          Usage: parsecookie.py -f /path/db.sqlite"
parser = argparse.ArgumentParser(usage=usage)

parser.add_argument("-f", "--filename", nargs="?", dest='database',
                    default=sys.stdin,
                    help="input a dbfile to process")
parser.add_argument('-o', '--output', default=sys.stdout,
                    type=argparse.FileType(mode='w'), nargs="?",
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

selectStatement = "SELECT host_key, name, creation_utc, expires_utc, last_access_utc FROM cookies"
cookiefile = args.database #args.filename()
con = sql.connect(cookiefile)
c = con.cursor()
for row in c.execute(selectStatement):
    print "cookie:",row[0].encode('utf-8')
    print "\tname:",str(row[1])
    print "\tcreation:",str(fixDate(row[2]))
    print "\texpires:",str(fixDate(row[3]))
    print "\tlastAccess:",str(fixDate(row[4]))

