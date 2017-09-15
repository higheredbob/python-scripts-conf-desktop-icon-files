#!/usr/bin/env python

import sys
import argparse
import sqlite3
import os.path
import os
import csv

parser = argparse.ArgumentParser(description="parse a dir cont. sqlite files")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase the output of information")
parser.add_argument("-d", "--dir", nargs="?", dest='dir',
                    default=sys.stdin, action="store",
                    help="input a dir to recursively walk through")
args = parser.parse_args()

mode = 'rb'
topdir = args.dir
exten = ""


def step():

    data = ""
    for dirpath, dirnames, filenames in os.walk(topdir):
        for files in filenames:
            # basename = os.path.basename(files)
            dirname = os.path.dirname(dirpath)
            # dirname = os.path.dirname(dirpath)
            names = os.path.basename(files)
            fname = os.path.join(dirpath, names)
            # db = sqlite3.connect(fname)
            # c = db.cursor()
            with open(fname, mode) as myfile:
                f = myfile
                f.seek(0)
            try:
                while 1:
                    if fname != "":
                        line = f.readline()
                    else:
                        line = sys.stdin.readline()
                    data += line
                    if not line:
                        break

                fetched = f.fetchall()
                if (fetched) > 0 :
                    for fe in fetched:
                        try:
                            aselectStatement = "SELECT fileID, relativePath, domain FROM Files"
                            conn = sql.connect(fname)
                            con = conn.cursor()
                            c = con.execute(aselectStatement)
                            rows = c.fetchall()
                            with open('args.outfile', 'w') as myfile:
                                for row in rows:
                                    writer = csv.writer(myfile,
                                                        quoting=csv.QUOTE_ALL)
                                    writer.writerow(row)
                        except:
                            print "likely not an sqlite file"
                            pass


                    def main():
                            step()

                    if __name__ == "__main__":
                            main()
