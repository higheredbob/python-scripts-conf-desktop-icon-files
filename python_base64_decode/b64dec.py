#!/usr/bin/env python

import re
import argparse
import sys
import os
import types
import struct
import array
from time import ctime
import base64

# detect base 64 via regex,
safestringre = re.compile('[\x80-\xFF]')
base1re = re.compile(r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)')
#base1re = re.compile('(^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$)')
#base1re = re.compile('(^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$)')
#base1re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)')
#base1re = re.compile('(?:[A-Za-z0-9+\/]{4}\\n?)*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)')
#base1re = re.compile('(^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)?)')
#base1re = re.compile(r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')

# define command line options
parser = argparse.ArgumentParser(description='read a file, search for base64 data to decode, output decoded data')
parser.add_argument('-i', '--infile', dest='infile', nargs='?', action='store',
                    help='input a strings or process dump to parse for base64 encoded data')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                    help='increase the verbal output')
args = parser.parse_args()


def safestring(badstring):
    """makes a good string out of a potentially bad one by escaping chars out of printable range
    """
    return safestringre.sub(lambda c: 'char#%d;' % ord(c.group(0)),badstring)


# housekeeping, checking infile and verbose
infile = args.infile

if infile == None:
    print('error, must specify an infile')
    sys.exit(1)

if infile != '':
    try:
        filehandle = open(infile, 'r')
        filehandle.close()
    except IOError:
        print('cannot open '+infile+', either corrupt or non-readable')
        sys.exit(1)

if args.verbose == True:
    print('\nparsing '+infile+' now')


def main():
    """main program, contains reading the infile, closing,
    data variables, and decoding function.
    """
    baseData = set()


    def base64decode(baseData):
        """function to correct padding on b64 data should it be
        missing, decode, the 2nd and 3rd (final attempt) at ascii error handling
        by urlsafe decoding and encoding to utf-8,
        printing is handled here because of the
        return for exceptions being an empty set, all out of range
        decoded characters that make it through the previous attempt
        at handling encoding are trapped here. Depending on the regex used,
        some may still make it through, however.
        """

        try:
            if baseData != '':
                baseData += "=" * ((4 - len(baseData) % 4) % 4)
                baseData = base64.urlsafe_b64decode(baseData)
                print "\ndecoded: " + baseData.encode('utf-8')
                return baseData

        except:
            return ''

    # open the file, ensure it starts at the begining
    if infile != '':
        f = open(infile, 'r')
        f.seek(0)

    # 1st attempt at encoding errors is done with re. through
    # escaping oor characters with safestring call, reads all
    # lines in file, and escapes oor characters.
    try:
        while 1:
            if infile != '':
                line = safestring(f.readline())
            if not line:
                break

            # reads infile, line by line, through safestring, using b64 regex of
            # those that match are stored in set, uniq's matches and for re
            # is the fastest python method for storing and retreiving data
            for line in f:
                match = base1re.match(line)
                if match is not None:
                    baseData.add(match.group())
                else:
                    if args.verbose == True:
                        print("bad string: "+line.strip())
                    continue

    except:
        print "error"

    # after b64 re. is finished searching and storing, this loop
    # itterates over the data, sorting it and sending it off for
    # attempted decoding
    for baseData in sorted(baseData):
        baseData = base64decode(baseData)

    # if for some odd reason the while statement does not close,
    # this statement checks if infile is still open and closes.
    if f:
        f.close()

if __name__=="__main__":
    main()
