#!/bin/sh
#

DB=singlePV.db
DATE=${1:-$(date  "+%Y-%m-%d")}

GESAMT=$(sqlite3 $DB "select max(dayTotalE) from single_measures where dateTime like '$DATE%'")
SAMPLES=$(sqlite3 $DB "select count(*) from single_measures where dateTime like '$DATE%'")
CASH=$(echo $GESAMT*0.43|bc)

gnuplot <<GNUPLOT
set title "DC Power am $DATE ($SAMPLES Messungen)"
set label "Tagesenergie: ${GESAMT}kWh \n(EUR $CASH)" at graph 0.03,0.9
set ylabel "Leistung in Watt"
set datafile separator "|"
set style data histograms
#set style data boxes
#set terminal png size 1024,600
set terminal pdf
set xtics rotate by -70
set grid 
set style fill
set output 'minutenVerlauf-single.pdf'
set xdata time
set timefmt x "%H:%M"
set format x "%H:%M"
#set xrange ["11:50":"12:00"]
set xtics 1800
plot '< sqlite3 $DB "select strftime(''%H:%M'',dateTime),dc1u*dc1i from single_measures where dateTime like ''$DATE%'' order by dateTime"' using 1:2 title "Garage String1" with lines, \
'< sqlite3 $DB "select strftime(''%H:%M'',dateTime),dc2u*dc2i from single_measures where dateTime like ''$DATE%'' order by dateTime"' using 1:2 title "Schuppen String2" with lines
GNUPLOT

open minutenVerlauf-single.pdf
