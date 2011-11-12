#!/bin/bash
#
# Zeigt Tagesverlauf der AC Leistung.
# Parameter: 2009-07-30 2009-08-02

DB=/home/thomas/toms-repo/Software/Wechselrichter/wechselrichter.db

echo "Content-type: image/png";echo

best=2011-05-09
DATES=${1:-$(date  "+%Y-%m-%d")}
DATES=${DATES//\\\&/ }

GESAMT=$(sqlite3 $DB "select round(sum(ac1p+ac2p+ac3p)/4000,1) from measures where dateTime like '$best%'")

plot="plot '< sqlite3 $DB \"select strftime(''%H:%M'',dateTime),ac1p+ac2p+ac3p from measures where dateTime like ''$best%'' order by zeit\"' using 1:2 smooth csplines title \"$best (${GESAMT}kWh)\" with lines"

for DATE in $DATES
do
    GESAMT=$(sqlite3 $DB "select round(sum(ac1p+ac2p+ac3p)/4000,1) from measures where dateTime like '$DATE%'")
    plot="$plot, '< sqlite3 $DB \"select strftime(''%H:%M'',dateTime),ac1p+ac2p+ac3p from measures where dateTime like ''$DATE%'' order by zeit\"' using 1:2 smooth csplines title \"$DATE (${GESAMT}kWh)\" with lines"
done


gnuplot <<GNUPLOT
set title "AC Power $DATES"
set ylabel "Leistung in Watt"
set datafile separator "|"
set style data histograms
set terminal png size 1000,600 enhanced transparent
set xtics rotate by 90
set grid 
set style fill
set output
set xdata time
set timefmt x "%H:%M"
set format x "%H:%M"
set xtics 1800
$plot
GNUPLOT
