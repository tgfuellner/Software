#!/bin/sh
#

#DB=/home/thomas/PV/singlePV.db
DB=/mnt/sd/PV/singlePV.db

DATE=${1:-$(date  "+%Y-%m-%d")}
DAYBEFORE=$(date "+%Y-%m-%d" --date "$DATE - 1 day")
NEXTDAY=$(date "+%Y-%m-%d" --date "$DATE + 1 day")

echo "Content-type: text/html";echo

echo "<html><head><title>History Wechselrichter</title></head><body>"
echo "$DATE<br><p>"

echo "<img src=\"minutenVerlauf-cgi.sh?$DATE\" alt=\"[Gnuplot Leistungsverlauf]\" align=\"middle\" border=\"0\">"

echo "<p><a href=\"hist.sh?$DAYBEFORE\"><--- </a>&nbsp;&nbsp;&nbsp;"
echo "<a href=\"hist.sh?$NEXTDAY\"> ---></a>"

echo "<p><a href=\"ueberLagertMinutenVerlauf-cgi.sh?$DAYBEFORE\">Vergleich</a>"

echo "<p>Tagesernete: <a href=\"tagesernte-cgi.sh\">Alles</a>&nbsp;&nbsp;"
echo "<a href=\"tagesernte-cgi.sh?2012\">2012</a>&nbsp;&nbsp;"
echo "<a href=\"tagesernte-cgi.sh?2011\">2011</a>&nbsp;&nbsp;"
echo "<a href=\"tagesernte-cgi.sh?2010\">2010</a>&nbsp;&nbsp;"
echo "<a href=\"tagesernte-cgi.sh?2009\">2009</a>"

echo "<p><a href=\"monatsernte-cgi.sh\">Monatsernte</a>&nbsp;&nbsp;"

echo "</body></html>"
