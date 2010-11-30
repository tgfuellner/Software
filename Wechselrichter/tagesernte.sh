#!/bin/sh
#

gnuplot <<GNUPLOT
set title "Tagesernte"
set ylabel "Leistung in kW"
set datafile separator "|"
set style data histograms
set terminal pdf
set grid 
set style fill
set output 'tagesernte.pdf'
set xtics rotate by 90 1

# Mit % 2 wird nur jedes zweite Datum mit einem Label versehen!
every(col) = (int(column(3)+1) % 4 == 0) ? stringcolumn(1) : ""

aa(col) = sprintf("%d",column(col))

plot '< sqlite3 wechselrichter.db "select strftime(''%Y-%m-%d'',datetime) date, sum(ac1p+ac2p+ac3p)/4000, strftime(''%j'',datetime) from measures where strftime(''%Y'', datetime) like ''20%'' group by date order by date"' using 2:xtic(every(3)) title "kWh" with histograms fs solid 0.3
GNUPLOT

open tagesernte.pdf
