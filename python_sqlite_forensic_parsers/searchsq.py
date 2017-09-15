#!/usr/bin/env python

import sys
import argparse
import sqlite3
import os.path
import os
import csv
import pandas as pd
from pandas import DataFrame, read_csv
# import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="parse a dir cont. sqlite files")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase the output of information")
parser.add_argument("-d", "--directPath", nargs="?", dest='directPath',
                    default=sys.stdin, action="store",
                    help="input a dir to recursively walk through")
args = parser.parse_args()

mode = 'rb'
topdir = args.directPath
exten = ""


def validateSQL(testingDB):
    #open file, confirm it is an SQLite DB

    try:
        if testingDB != "":
            f=open(testingDB,"r")
        elif testingDB != "":
            f=open(testingDB, "rb")
    except:
            print "file is neither utf or binary sqlite"
            f=close(testingDB)
            raise argparse.ArgumentTypeError('file is not present or not SQLite')


    f.seek(0)
    verifyHeader = f.read(16)
    if "SQLite" not in verifyHeader:
        print ("file is not a SQL or been apeRaped")
        raise argparse.ArgumentTypeError('file was opened and read, no SQLite in header')
    else:
        offset = 0
        stats = os.stat(testingDB)
        filesize = stats.st_size
        f.seek(0)
        f.close()
        validatedDB = testingDB

        return validatedDB


def openOut(outPath, outCSV):
    try:
        output = (args.outdir, 'w')
    except:
        print "Error opening output file"
        sys.exit(0)


def CSVwriter(db):

    selection = "SELECT fileID, relativePath, domain FROM Files"
    db = sqDB

def step(topdir):

    inPath = []
    nameDB = []
    for dirpath, dirnames, filenames in os.walk(topdir):
        for files in filenames:
            inPath = os.path.dirname(dirpath)
            nameDB = os.path.basename(files)
            if os.path.isfile(files):
                nameDB(append(files))
            elif os.path.isdir(files):
                inPath(append(files))

            return nameDB, inPath


    def pandasql():

        step(topdir)
        mastPath = []
        j = os.path.join[dirsf, filesf]
        mastPath.append(j)


        fileSQL = []
        otherF = []
        testingDB = mastPath
        for files in testingDB:
            if files != "":
                validateSQL(files)

                if os.path.isfile(validatedDB):
                    fileSQL.append(validatedDB)

                    for dbs in fileSQL:

                        db = sqlite3.connect(dbs)
                        query = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        cols = [column[0] for column in query.description]
                        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
                        print results
            #cur = db.cursor()

            #cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            #rows = cur.fetchall()
            #for row in rows:
            #    rowName = rowName[0]
            #    row = pd.read_sql_query('SELECT * from %s' % rowName, db)
            #    cols = [column[0] for column in query.description]
            #    results = pd.DataFrame.from_records(data = rows(), columns = cols)



def main():
        step(topdir)

if __name__=="__main__":
    main()
