#!/usr/bin/env python

"""schema and full dump of any sqlite db
"""
import sqlite3 as sql
import sys
import argparse
import csv, codecs, cStringIO
import os

parser = argparse.ArgumentParser(description="input a sqlite database, it will query the tables and schema,\n\
and either print or save to a csv file a dump of the database")
parser.add_argument('-f', '--filename', dest="database", nargs="?",
                    action="store", help="db to process")
parser.add_argument('-o', '--outfile', dest="outfile", nargs="?", action="store",
                    default=sys.stdout, help="path to output csv file, defaults to stdout if no flag")
parser.add_argument('-v', '--verbose', action="store_true", default=False,
                    help="increase verbal output")
args = parser.parse_args()
db = args.database
outfile = args.outfile
verb = args.verbose
    #help = args.help



class CSVWriter:

    def __init__(self, csvFile, heading):
        try:
            # create a writer object and then write the header row
            self.csvFile = open(csvFile, 'w')
            self.writer = csv.writer(self.csvFile, delimiter=',',quoting=csv.QUOTE_ALL)
            self.writer.writerow(heading)
        except:
            print "CSV File: Initialization Failed"
            sys.exit(1)

    def writeCSVRow(self, row):
        try:
            rowList = []
            for item in row:

                if type(item) == unicode or type(item) == str:
                    item = item.encode('ascii','ignore')

                rowList.append(item)

            self.writer.writerow(rowList)

        except:
            print "CSV File Write: Failed"
            sys.exit(1)

    def __del__(self):
        # Close the CSV File
        try:
            self.csvFile.close()
        except:
            print "Failed to close CSV File Object"
            sys.exit(1)


if db == None:
    print 'error, must input a db to process'
    print help
    sys.exit(1)

if not os.path.isdir(outfile):
    os.makedirs(outfile)

if verb == True:
    print 'Processing Datbase: ' + db


try:
    selectStatement = "SELECT name FROM sqlite_master WHERE type = \"table\""

    con = None
    con = sql.connect(db)
    c = con.cursor()
    c.execute(selectStatement)
    tableTuple = c.fetchall()
    for table in tableTuple:
        if verb == True:
            print(table[0])


    c.execute("SELECT * from " + table[0])
    for item in tableTuple:
        tableName = item[0]
        if verb == True:
            print("writing Table: "+tableName+"\n")
        tableQuery = "SELECT * FROM "+tableName
        c.execute(tableQuery)
        tableDescription = c.description
        tableHeading = []
        for item in tableDescription:
            tableHeading.append(item[0])

        #f = open(outfile+"/"+tableName+".csv", 'wb')
        tCSV = CSVWriter(outfile+"/"+tableName+".csv", tableHeading)

        rowData = c.fetchall()

        for row in rowData:
            tCSV.writeCSVRow(row)

        tCSV.__del__()

except:
    print("sql error")
    sys.exit(1)

finally:

    if con:
        con.close()


