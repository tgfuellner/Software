#!/bin/bash
#

DB=/home/pi/PV/wechselrichter.db
YEAR=${1:-20}
YEAR_BEFORE=$[$YEAR-1]

if [ $YEAR = "20" ]
then
 DATE_LABEL_MODULO=30
else
 DATE_LABEL_MODULO=14
fi 

echo "Content-type: image/png";echo

gnuplot <<GNUPLOT
set title "Tagesernte"
set ylabel "Leistung in kWh"
set datafile separator "|"
set style data histograms
set terminal png size 1000,600 enhanced
#set grid 
set style fill
set output
set xtics rotate by 90 1

# Mit % 2 wird nur jedes zweite Datum mit einem Label versehen!
every(col) = (int(column(3)+1) % $DATE_LABEL_MODULO == 0) ? stringcolumn(1) : ""

aa(col) = sprintf("%d",column(col))

plot '< sqlite3 $DB "select strftime(''%Y-%m-%d'',datetime) date, sum(ac1p+ac2p+ac3p)/4000, strftime(''%j'',datetime) from measures where strftime(''%Y'', datetime) like ''$YEAR%'' group by date order by date"' using 2:xtic(every(3)) title "$YEAR" with histograms fs solid 0.3, \
'< sqlite3 $DB "select strftime(''%Y-%m-%d'',datetime) date, sum(ac1p+ac2p+ac3p)/4000, strftime(''%j'',datetime) from measures where strftime(''%Y'', datetime) like ''$YEAR_BEFORE%'' group by date order by date"' using 2:xtic(every(3))  lt rgb "gray" title "$YEAR_BEFORE" with histograms 

GNUPLOT
