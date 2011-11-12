#!/bin/sh
#

DB=/home/thomas/toms-repo/Software/Wechselrichter/wechselrichter.db

echo "Content-type: image/png";echo

gnuplot <<GNUPLOT
set title "Monatsernte"
set ylabel "Leistung in kWh"
set datafile separator "|"
set style data histograms
set terminal png size 1000,600 enhanced transparent
set grid 
set style fill
set output
set xtics rotate by 90
plot '< sqlite3 $DB "\
select a.month, a.energie-b.energie from \
	(select (strftime(''%Y'',dateTime)-2009)*12+strftime(''%m'',dateTime) m, \
        strftime(''%Y-%m'',dateTime) month, max(totalE) energie \
		from measures  where totalE <> '."''".' group by m) as a,\
	(select (strftime(''%Y'',dateTime)-2009)*12+strftime(''%m'',dateTime) m, \
        strftime(''%Y-%m'',dateTime) month, max(totalE) energie \
		from measures  where totalE <> '."''".' group by m) as b \
where a.m+0 = b.m+1 \
order by a.m\
"' using 2:xtic(1) title "kWh" with histograms fs solid 0.3
GNUPLOT
