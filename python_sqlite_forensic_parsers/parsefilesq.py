#!/usr/bin/python

import datetime
import sqlite3 as sql
import argparse
import sys
import time
import encodings


parser = argparse.ArgumentParser(description="parse a dir cont. sqlite files")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase the output of information")
parser.add_argument("-f", "--filename", nargs="?", dest='database',
                    default=sys.stdin,
                    help="input a dbfile to process")
args = parser.parse_args()

db = args.database

def fixDate(timestamp):
    #Chrome stores timestamps in the number of microseconds since Jan 1 1601.
    #To convert, we create a datetime object for Jan 1 1601...
    epoch_start = datetime.datetime(1601,1,1)
    #create an object for the number of microseconds in the timestamp
    delta = datetime.timedelta(microseconds=int(timestamp))
    #and return the sum of the two.
    return epoch_start + delta
    #datetime(media_time/1000, 'unixepoch', 'localtime') AS date FROM media_record

selectStatement = "SELECT metahandle, base_version, datetime(mtime/1000, 'unixepoch', 'localtime') AS Mdate, datetime(server_mtime/1000, 'unixepoch', 'localtime') AS Mserver, datetime(ctime/1000, 'unixepoch', 'localtime') AS Ctime, datetime(server_ctime/1000, 'unixepoch', 'localtime') AS Cserver, specifics FROM metas"
# thumbsfile = args.database #args.filename()
con = sql.connect(db)
c = con.cursor()
c.execute(selectStatement)
rows = c.fetchall()
for row in rows:
    metahandle, base_version, Mdate, Mserver, Ctime, Cserver, specifics = row
    #print(row[6].encode('utf-8'))
    print ('{}|{}|{}|{}|{}|{}|{}.encode("utf-8")'.format(metahandle, base_version, Mdate, Mserver, Ctime, Cserver, specifics.decode('utf-8')))
#con = sql.connect(db)
#c = con.cursor()
#for row in c.execute(selectStatement):
#    print "id:",int(row[0])
#    print "\tbase:",str(row[1])
#    print "\tcreation:",str(fixDate(row[2]))
#    print "\tservercreate:",str(fixDate(row[3]))
#    print "\tCcreate:",str(fixDate(row[4]))
#    print "\tCservercreate:",str(fixDate(row[5]))
#    print "\tCcreate:",str(row[6])
    #row[6].encode('utf-8')
