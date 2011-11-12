#!/bin/sh
#
# Zeigt Tagesverlauf der AC Leistung.
# Parameter: 2009-07-30 2009-08-02

best=2010-06-05
DATE=${1:-$(date  "+%Y-%m-%d")}
shift

GESAMT=$(sqlite3 wechselrichter.db "select round(sum(ac1p+ac2p+ac3p)/4000,1) from measures where dateTime like '$DATE%'")

plot="plot '< sqlite3 wechselrichter.db \"select strftime(''%H:%M'',dateTime),ac1p+ac2p+ac3p from measures where dateTime like ''$DATE%'' order by zeit\"' using 1:2 smooth csplines title \"$DATE (${GESAMT}kWh)\" with lines"

for DATE in $* $best
do
    GESAMT=$(sqlite3 wechselrichter.db "select round(sum(ac1p+ac2p+ac3p)/4000,1) from measures where dateTime like '$DATE%'")
    plot="$plot, '< sqlite3 wechselrichter.db \"select strftime(''%H:%M'',dateTime),ac1p+ac2p+ac3p from measures where dateTime like ''$DATE%'' order by zeit\"' using 1:2 smooth csplines title \"$DATE (${GESAMT}kWh)\" with lines"
done


gnuplot <<GNUPLOT
set title "AC Power"
set ylabel "Leistung in Watt"
set datafile separator "|"
set style data histograms
set terminal pdf
set xtics rotate by -70
set grid 
set style fill
set output 'ueberLagertMinutenVerlauf.pdf'
set xdata time
set timefmt x "%H:%M"
set format x "%H:%M"
set xtics 1800
$plot
GNUPLOT

evince ueberLagertMinutenVerlauf.pdf
