#!/usr/bin/env python

import datetime
import sqlite3 as sql
import argparse
import sys
import time
import pandas as pd
import pandas

parser = argparse.ArgumentParser(description="parse a dir cont. sqlite files")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase the output of information")
parser.add_argument("-f", "--filename", nargs="?", dest='database', 
                    default=sys.stdin, action="store",
                    help="input a dbfile to process")
args = parser.parse_args()




db = args.database
con = sql.connect(db)
c = con.cursor()
_left_f = pandas.read_sql_query("SELECT * FROM moz_favicons", con)
_right_f = pandas.read_sql_query("SELECT * FROM moz_historyvisits", con)
_aRight_f = pandas.read_sql_query("SELECT * FROM moz_anno_attributes", con)
_bRight_f = pandas.read_sql_query("SELECT * FROM moz_annos", con)
_cRight_f = pandas.read_sql_query("SELECT * FROM moz_hosts", con)
_dRight_f = pandas.read_sql_query("SELECT * FROM moz_inputhistory", con)
_eRight_f = pandas.read_sql_query("SELECT * FROM moz_items_annos", con)
_fRight_f = pandas.read_sql_query("SELECT * FROM moz_keywords", con)
_gRight_f = pandas.read_sql_query("SELECT * FROM moz_places", con)
_hRight_f = pandas.read_sql_query("SELECT * FROM moz_bookmarks", con)
_iRight_f = pandas.read_sql_query("SELECT * FROM moz_bookmarks_roots", con)
_jRight_f = pandas.read_sql_query("SELECT * FROM moz_favicons", con)
#varSelect = pd.merge(_left_f, _right_f, on='', how='outer')
#select * from (bdg left join res on bdg.id = res.id) left join dom on res.rid = dom.rid;
#varSelect = "SELECT * FROM (moz_historyvisits LEFT JOIN moz_places ON moz_historyvisits.rowid = moz_places.rowid) LEFT JOIN moz_hosts ON moz_places.frecency = moz_hosts.frecency"    

#aStatement = pd.merge(cSelect, dSelect, on='id', how='left')
#bStatement = pd.merge(aSelect, bSelect, on='id', how='left')
#selectStatement = pd.merge(bStatement, aStatement, on='id', how='left')
#varp = con.varSelect()
ajoin = pd.merge(_jRight_f, _bRight_f, on='mime_type', how='left')
bjoin = pd.merge(_aRight_f, _fRight_f, on='id', how='right')
#print "\nva:",str(ajoin)
print ajoin
print bjoin
#print "\nr:",str(_right_f)
#print "\nr:",str(_aRight_f)
#print "\nr:",str(_bRight_f)
#print "\nr:",str(_cRight_f)
#print "\nr:",str(_dRight_f)
#print "\nr:",str(_eRight_f)
#print "\nr:",str(_fRight_f)
#print "\nr:",str(_gRight_f)
#print "\nr:",str(_hRight_f)
#print "\nr:",str(_iRight_f)
#c = con.cursor()
#data = c.execute(varSelect)
#rows = c.fetchall()
#for row in rows:
#    try:
#        rowList = {}
        
#    print("row: %s" % (row)) 
