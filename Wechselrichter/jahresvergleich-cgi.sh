#!/bin/bash
#

DB=/mnt/nas/wechselrichter.db

DATE_LABEL_MODULO=1

echo "Content-type: image/png";echo

gnuplot <<GNUPLOT
set title "Tagesernte"
set ylabel "Leistung in kWh"
set datafile separator "|"
set style data histograms
set terminal png size 1000,600 enhanced transparent
#set grid 
set style fill
set output
#set xtics rotate by 90 1

# Mit % 2 wird nur jedes zweite Datum mit einem Label versehen!
every(col) = (int(column(3)+1) % $DATE_LABEL_MODULO == 0) ? stringcolumn(1) : ""

aa(col) = sprintf("%d",column(col))

plot '< sqlite3 $DB "select strftime(''%Y'',datetime) date, sum(ac1p+ac2p+ac3p)/4000, strftime(''%j'',datetime) from measures group by date order by date"' using 2:xtic(every(3)) title "Alles" with histograms fs solid 0.3


GNUPLOT
