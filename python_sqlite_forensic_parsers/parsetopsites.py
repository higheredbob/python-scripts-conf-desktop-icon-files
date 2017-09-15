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

selectStatement = "SELECT url, title, last_updated, datetime(last_updated/1000000-11644473600, 'unixepoch', 'localtime') as Datet, load_completed, redirects FROM thumbnails"
thumbsfile = args.database #args.filename()
con = sql.connect(thumbsfile)
c = con.cursor()
#for row in c.execute(selectStatement):
c.execute(selectStatement)
rows = c.fetchall()
for row in rows:
    #last_updated = "lastUpdated",str(fixDate(row[2]))
    url, title, last_updated, Datet, load_completed, redirects = row
    #print "url:",row[0].encode('utf-8')
    #print "\ttitle:",str(row[1])
    #print "\tlastUpdated:",str(fixDate(row[2]))
    #print "\tcompleted:",str(row[3])
    #print "\tredirects:",str(row[4])
    print("\nurl: {},\n\ttitle: {},\n\tlastUpdated: {},\n\tDate: {},\n\tloadComplete: {},\n\tRedirects: {}|".format(url, title, fixDate(last_updated), Datet, load_completed, redirects))
