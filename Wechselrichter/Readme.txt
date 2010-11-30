Datenformat für sonnenertrag.eu:
    http://www.photovoltaikforum.com/viewtopic.php?p=163723#163723

Wechselrichter Daten holen:
     wget --user=pvserver --password=sonne http://192.168.0.48/LogDaten.dat
     wget http://pvserver:sonne@192.168.0.48/LogDaten.dat


select datetime,ac1p+ac2p+ac3p from measures where datetime like '2009-07-27%' order by datetime;

Tagesleistung:
select sum(ac1p+ac2p+ac3p)/4000,'kW' from measures where datetime like '2009-07-27%' order by datetime;
select date(datetime) date, sum(ac1p+ac2p+ac3p)/4000 from measures group by date;
select date(datetime), totalE from measures where totalE is not null;

gnuplot:
set style data lines
set datafile separator "|"
set style data histograms
set terminal png size 1024,600
set output 'tagesernte.png'
plot "< sqlite3 wechselrichter.db 'select date(datetime) date, sum(ac1p+ac2p+ac3p)/4000 from measures group by date order by date'" using 2:xtic(1) title "kWh"
