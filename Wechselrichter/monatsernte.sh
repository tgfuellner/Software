#!/bin/sh
#

gnuplot <<GNUPLOT
set title "Monatsernte"
set ylabel "Leistung in kW"
set datafile separator "|"
set style data histograms
set terminal pdf
set grid 
set style fill
set output 'monatsernte.pdf'
set xtics rotate by -70
plot '< sqlite3 wechselrichter.db "\
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

# Wenn nur ein Jahr gewünscht:
# where a.m+0 = b.m+1 and a.month like ''2009%''\

open monatsernte.pdf
