#!/usr/bin/python2

import urllib
from datetime import datetime
from datetime import timedelta
from pysqlite2 import dbapi2 as sqlite

# Messwerte pro Zeile im Logfile
NR_OF_MEASURES = 42

connection = sqlite.connect('/home/pi/PV/wechselrichter.db')
cursor = connection.cursor()

# ------------------------------------------------
# Create Database relations

stmt = """
    CREATE TABLE IF NOT EXISTS timePoints (
        seconds INTEGER PRIMARY KEY
        ,dateTime VARCHAR(50)
    )
"""
cursor.execute(stmt)

stmt = """
    CREATE TABLE IF NOT EXISTS measures (
          dateTime VARCHAR(50)
         ,Zeit INTEGER
         ,DC1U integer, DC1I integer, DC1P integer, DC1T integer, DC1S integer
         ,DC2U integer, DC2I integer, DC2P integer, DC2T integer, DC2S integer
         ,DC3U integer, DC3I integer, DC3P integer, DC3T integer, DC3S integer
         ,AC1U integer, AC1I integer, AC1P integer, AC1T integer, AC2U integer
         ,AC2I integer, AC2P integer, AC2T integer, AC3U integer, AC3I integer
         ,AC3P integer, AC3T integer, ACF real, FCI integer, Ain1 integer
         ,Ain2 integer, Ain3 integer, Ain4 integer, ACS integer, Err integer
         ,ENSS integer, ENSErr integer
         ,KBS VARCHAR(15), totalE integer, IsoR integer, Ereignis VARCHAR(10)
         ,dayTotalE integer
    )
"""
cursor.execute(stmt)



# ------------------------------------------------

# Hole Daten vom Wechselrichter
def fetchLog():
    nun = datetime.now()
    sock = urllib.urlopen("http://pvserver:sonne@192.168.0.48/LogDaten.dat")
    # sock = open("LogDaten.dat")
    lineList = sock.readlines()
    sock.close()
    return (lineList, nun)

def myDateFormat(nun):
    return nun.strftime('%Y-%m-%d %H:%M:%S')

# Aktuelle Timestamp, Sekunden seit Inbetriebname des WR
# der aktuellen Uhrzeit und Datum zuordnen.
# Im LogDaten.dat steht:
# akt. Zeit:	    351796
def insertTimePoint(timePointLine, jetzt):
    global cursor
    global connection

    assert timePointLine.find("Zeit") > 0
    requestTime = timePointLine.split()[2]

    print("Timestamp = "+requestTime+"s = "+jetzt.isoformat())

    cursor.execute("""INSERT INTO timePoints (seconds,datetime) VALUES 
        (?, ?)""" , (requestTime,myDateFormat(jetzt)))
    connection.commit()
    return requestTime

def insertMeasure(logTimeInSeconds, nun, records):
    global cursor
    global connection
    global NR_OF_MEASURES

    recordSeconds = records[0]

    cursor.execute("select count(*) from measures where zeit=?", (recordSeconds,))
    if cursor.fetchone()[0] > 0:
        return False

    d = timedelta(seconds=int(logTimeInSeconds)-int(recordSeconds))
    nun = nun - d
    values = [myDateFormat(nun)] + records + ['']

    p = ('?',)*(NR_OF_MEASURES+2)
    cursor.execute("INSERT INTO measures VALUES (" + ','.join(p) + ")", values)

    return True


class BackReader:
    """Gibt Zeilen in umgekehrter Reihenfolge wieder"""

    def __init__(self, lines):
        self.lines = lines
        self.pos = 0

    def next(self):
        global NR_OF_MEASURES

        self.pos -= 1
        line = self.lines[self.pos].split('\t')
        line = [item.strip() for item in line]
        if line[0] == "Zeit":
            return ()
        else:
            line.extend((None,)*4)
            line = line[0:NR_OF_MEASURES]
            return line

# ------------------------------------------------

(lineList,nun) = fetchLog()
if len(lineList) < 100:
    # Der HTTP-Server auf dem Wechselrichter hat Probleme 
    # mit dem ersten Request!
    (lineList, nun) = fetchLog()

logTimeInSeconds = insertTimePoint(lineList[3], nun)

br = BackReader(lineList)
n = 0
line = br.next();
while line:
    if insertMeasure(logTimeInSeconds, nun, line) == False:
        break
    n += 1
    line = br.next()

connection.commit()

print n, u"Messungen angehaengt"


cursor.close()
connection.close()


