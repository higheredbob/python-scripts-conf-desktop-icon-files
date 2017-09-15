"""
https://jon.glass/
"""

import sqlite3, datetime
selectStatement = 'SELECT * FROM ItemTable'
LocalStorageFile = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Storage\\https_jon.glass_0.localstorage' 
c = sqlite3.connect(LocalStorageFile)
for row in c.execute(selectStatement):
    print row[0]
    print str(row[1]).decode("utf-16")