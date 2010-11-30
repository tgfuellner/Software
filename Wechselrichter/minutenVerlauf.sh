#!/bin/sh
#

DATE=${1:-$(date  "+%Y-%m-%d")}

GESAMT=$(sqlite3 wechselrichter.db "select round(sum(ac1p+ac2p+ac3p)/4000,1) from measures where dateTime like '$DATE%'")
GARAGE=$(sqlite3 wechselrichter.db "select round(sum(dc1p)/4000,1) from measures where dateTime like '$DATE%'")
SCHUPPEN=$(sqlite3 wechselrichter.db "select round(sum(dc2p)/4000,1) from measures where dateTime like '$DATE%'")
CASH=$(echo $GESAMT*0.43|bc)

echo $GARAGE $SCHUPPEN

gnuplot <<GNUPLOT
set title "DC Power am $DATE"
set label "Einspeisung: ${GESAMT}kWh (EUR $CASH)\nGarage = ${GARAGE}kWH\nSchuppen = ${SCHUPPEN}kWh" at graph 0.03,0.96
set ylabel "Leistung in Watt"
set datafile separator "|"
set style data histograms
#set style data boxes
#set terminal png size 1024,600
set terminal pdf
set xtics rotate by -70
set grid 
set style fill
set output 'minutenVerlauf.pdf'
set xdata time
set timefmt x "%H:%M"
set format x "%H:%M"
set xtics 1800
plot '< sqlite3 wechselrichter.db "select strftime(''%H:%M'',dateTime),dc1p from measures where dateTime like ''$DATE%'' and dc1p <>'."''".' order by zeit"' using 1:2 smooth csplines title "Garage String1" with lines, \
'< sqlite3 wechselrichter.db "select strftime(''%H:%M'',dateTime),dc2p from measures where dateTime like ''$DATE%'' and dc2p <>'."''".'  order by zeit"' using 1:2 smooth csplines title "Schuppen String2" with lines
GNUPLOT

open minutenVerlauf.pdf
