#!/usr/bin/env python
# Import the standard library module sqlite3
# This type of import allows you to abbreviate the interface
# to sql methods.   i.e. sql.connect  vs sqlite3.connect
import sqlite3 as sql
import sys
import csv
import os
import argparse


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


class Display():

    def __init__(self, verbose):
        self.verbose = verbose
        self.ver = sys.version_info

    def Print(self, msg):
        if self.verbose:

            if self.ver >= (3,0):
                print(msg)
            else:
                print msg


def ParseCommandLine():

    parser = argparse.ArgumentParser('SQL DB Dump')

    parser.add_argument('-v', '--verbose', help="enables printing of additional program messages", action='store_true')
    parser.add_argument('-i', '--sqlDB',   type= ValidateFileRead,  required=True, help="input filename of the sqlite database")
    parser.add_argument('-o', '--outPath', type= ValidateDirectory, required=True, help="output path for extracted tables")

    theArgs = parser.parse_args()

    return theArgs


def ValidateFileRead(theFile):

    # Validate the path is a valid
    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File does not exist')

    # Validate the path is readable
    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File is not readable')


def ValidateDirectory(theDirectory):

    # Validate the path is a valid directory
    if not os.path.exists(theDirectory):
        raise argparse.ArgumentTypeError('Directory does not exist')

    # Validate the path is writable
    if os.access(theDirectory, os.W_OK):
        return theDirectory
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')


def main(verboseFlag, theDB, outPath):

    p = Display(verboseFlag)
    p.Print("Python Forensics: SQLite Investigation Part One - Simple Database Dump")

    try:
        db = None
        db = sql.connect(theDB)
        dbCursor = db.cursor()
        dbCursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tableTuple = dbCursor.fetchall()
        p.Print("Tables Found")

        for table in tableTuple:
            p.Print(table[0])
        for item in tableTuple:
            tableName = item[0]
            p.Print("Processing Table: "+tableName+"\n")
            tableQuery = "SELECT * FROM "+tableName
            dbCursor.execute(tableQuery)
            tableDescription = dbCursor.description
            tableHeading = []
            for item in tableDescription:
                tableHeading.append(item[0])

            oCSV = CSVWriter(outPath+os.sep+tableName+'.csv', tableHeading)

            rowData = dbCursor.fetchall()
            for row in rowData:
                oCSV.writeCSVRow(row)

            oCSV.__del__()

    except:
        p.Print ("SQL Error")
        sys.exit(1)

    finally:

        if db:
            db.close()

    p.Print("End Program")


if __name__ == "__main__":

    args = ParseCommandLine()

    # Call main passing the user defined arguments

    main(args.verbose, args.sqlDB, args.outPath)
