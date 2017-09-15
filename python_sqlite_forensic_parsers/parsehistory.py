#!/usr/bin/python

"""for the chrome history file.
"""

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

#selectStatement = "SELECT lower_term, term, url_id FROM keyword_search_terms"
db = args.database #args.filename()

    
aselectStatement = "SELECT id, url, title, visit_count, typed_count, last_visit_time FROM urls ORDER BY last_visit_time ASC"
con = sql.connect(db)
c = con.cursor()
for row in c.execute(aselectStatement):
    print "id:",str(row[0])
    print "\turl:",str(row[1])
    print "\ttitle:",row[2].encode('utf-8')
    print "\tvisits:",str(row[3])
    print "\ttyped:",str(row[4])
    print "\tlast_visit:",str(fixDate(row[5]))
    
