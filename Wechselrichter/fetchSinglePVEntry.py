#!/opt/local/bin/python

import urllib
import time
from datetime import datetime
from datetime import timedelta
from pysqlite2 import dbapi2 as sqlite
from HTMLParser import HTMLParser
from optparse import OptionParser

# Messwerte auf der HTML Seite
NR_OF_MEASURES = 13


# ------------------------------------------------
# Create Database relations
def createRelations(curs):
    stmt = """
    CREATE TABLE IF NOT EXISTS timePoints (
        seconds INTEGER PRIMARY KEY
        ,dateTime VARCHAR(50)
    )
    """
    curs.execute(stmt)

    stmt = """
    CREATE TABLE IF NOT EXISTS single_measures (
          dateTime VARCHAR(50)
         ,DC1U integer, DC1I integer
         ,DC2U integer, DC2I integer
         ,AC1U integer, AC1P integer, AC2U integer
         ,AC2P integer, AC3U integer
         ,AC3P integer 
         ,totalE integer
         ,dayTotalE integer
    )
    """
    curs.execute(stmt)



# ------------------------------------------------

# Hole Daten vom Wechselrichter
def fetchPage():
    nun = datetime.now()
    sock = urllib.urlopen("http://pvserver:sonne@192.168.0.48/index.fhtml")
    # sock = open("LogDaten.dat")
    page = sock.read()
    sock.close()
    return (page, nun)

def myDateFormat(nun):
    return nun.strftime('%Y-%m-%d %H:%M:%S')


# ------------------------------------------------


class Spider(HTMLParser):
    def __init__(self, page):
        HTMLParser.__init__(self)
        self.valueList = []
        self.feed(page)

    def handle_data(self, data):
        data = data.strip()
        if data == '':
            return

        try:
            float(data)
        except ValueError:
            return

        self.valueList.append(data)

    def getValues(self):
        return self.valueList



def insertValues(nun, values):
    values[0] = myDateFormat(nun)

    p = ('?',)*NR_OF_MEASURES

    cursor.execute("""
    INSERT INTO single_measures
        (dateTime,totalE,dayTotalE,DC1U,AC1U,DC1I,AC1P,DC2U,AC2U,DC2I,AC2P,AC3U,AC3P)
    VALUES (""" + ','.join(p) + ")", values)

def printValues(wantHtml, values):
    PREIS = 0.43
    (acpTotal,totalE,dayTotalE,DC1U,AC1U,DC1I,AC1P,DC2U,AC2U,DC2I,AC2P,AC3U,AC3P) = values
    # print locals()

    if wantHtml:
        print "Content-type: text/html\n"
	print "<html><head><title>Wechselrichter</title></head><body>"

    print acpTotal, "W = Leistung aktuell"
    if wantHtml:
	print "<br>",
    print dayTotalE, "kWh = Tagesenergie = ", float(dayTotalE)*PREIS, "EUR"
    if wantHtml:
	print "<br>",
    e = int(totalE) - 413
    print e, "kWh = Einspeisung gesamt = ", e*PREIS, "EUR"

    if wantHtml:
        print "<p>"
        print '<img src="minutenVerlauf-cgi.sh" alt="[Gnuplot Leistingsverlauf]" align="middle" border="0">'
	print "</body></html>"

######################## Main #########################
        
parser = OptionParser()
parser.add_option("-l", "--loop", dest="loopInterval",
                  type="int",
                  help="Fetch values every N seconds", metavar="N")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print values to stdout")
parser.add_option("-m", "--html",
                  action="store_true", dest="html", default=False,
                  help="Markup Values in HTML format")
parser.add_option("-d", "--database", dest="DataBase",
                  type="string", default="/mnt/sd/PV/singlePV.db",
                  help="Store data fom the Wechselrichter to database", metavar="database")

(options, args) = parser.parse_args()

connection = sqlite.connect(options.DataBase)
cursor = connection.cursor()

createRelations(cursor)

while 1:
    (page,nun) = fetchPage()
    sp = Spider(page)

    if len(sp.getValues()) == 13:
        if options.verbose:
            printValues(options.html, sp.getValues())
        insertValues(nun, sp.getValues())
        connection.commit()
    else:
        l = ['xxx',]*13
        (totalE,dayTotalE) = sp.getValues()
        l[1] = totalE
        l[2] = dayTotalE
        printValues(options.html, l)
        if not options.html:
            print "Es wird gerade nicht eingespeist!?"

    if options.loopInterval:
        time.sleep(options.loopInterval)
    else:
        break
    

cursor.close()
connection.close()



