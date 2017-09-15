#!/usr/bin/env python

import sqlite3 as sql
import argparse
import csv
import sys
import os

parser = argparse.ArgumentParser(description="get schema info, metadata, and queries, input a sql db \n\
and output file for csv txt file")
parser.add_argument('-f', '--filedb', nargs="?", dest="filedb",
                    action="store", help="input sqldb")
parser.add_argument('-o', '--outdir', nargs="?", dest="outdir",
                    action="store", default=sys.stderr, help="output dir")
args = parser.parse_args()

db = args.filedb
output = args.outdir

if not os.path.exists(output):
    os.mkdir(output)


def schemapull(db, output):

        selState = "SELECT name FROM sqlite_master WHERE type='table';"
        con = sql.connect(db)
        c = con.cursor()
        c.execute(selState)
        tableTuple = c.fetchall()
        for table in tableTuple:
            print(table[0])
        for item in tableTuple:
            tableName = item[0]
            print("found table: " + tableName +"\n")
            tableQuery = "SELECT * FROM "+tableName
            c.execute(tableQuery)
            tableDescription = c.description
            tableHeading = []
            for item in tableDescription:
                tableHeading.append(item[0])

        if tableHeading != '':
            outpath = output+tableName+'.csv'
            csvO = open(outpath, 'w')
            writer = csv.writer(csvO, delimiter=',',quoting=csv.QUOTE_MINIMAL)
            writer.writerows(tableHeading)
            rowdata = c.fetchall()
            for row in rowdata:
                if row != '':
                    rowList = []
                    for item in row:
                        if type(item) == unicode or type(item) == str:
                            item = item.encode('ascii', 'ignore')
                        rowList.append(item)
                        writer.writerows(rowList)


            csvO.close()
        c.close()


def main():
    schemapull(db, output)

if __name__=="__main__":
    main()
