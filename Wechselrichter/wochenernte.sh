#!/bin/sh
#

gnuplot <<GNUPLOT
set title "Wochenernte"
set ylabel "Leistung in kW"
set datafile separator "|"
set style data histograms
set terminal pdf
set grid 
set style fill
set output 'wochenernte.pdf'
set xtics rotate by -70
plot '< sqlite3 wechselrichter.db "\
select a.week, a.energie-b.energie from \
	(select (strftime(''%Y'',dateTime)-2009)*52+strftime(''%W'',dateTime) m, \
        strftime(''%Y %W'',dateTime) week, max(totalE) energie \
		from measures  where totalE <> '."''".' group by m) as a,\
	(select (strftime(''%Y'',dateTime)-2009)*52+strftime(''%W'',dateTime) m, \
        strftime(''%Y %W'',dateTime) week, max(totalE) energie \
		from measures  where totalE <> '."''".' group by m) as b \
where a.m+0 = b.m+1 \
order by a.m\
"' using 2:xtic(1) title "kWh" with histograms fs solid 0.3
GNUPLOT

open wochenernte.pdf
