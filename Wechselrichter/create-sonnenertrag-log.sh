#!/bin/sh

# Erzeugt min_day.js
# Für sonnenertrag.eu
# Siehe: http://www.photovoltaikforum.com/viewtopic.php?p=163723#163723

sqlite3 wechselrichter.db "select strftime('m[mi++]=\"%d.%m.%Y %H:%M:%S',dateTime),\
    ac1p+ac2p+ac3p, dc1p+dc2p,\
    'ertrag in Wh',\
    dc1u, 0 \
 from measures\
 where dateTime like '2009-08-01%'\
 order by zeit asc" \
| awk -F '|' '{sum += $2} {printf "%s|%s;%s;%s;%s;%s\"\n",$1,$2,$3,int(sum/4),$5,$6}' \
| sed -e 's/\([0-9][0-9]\.[0-9][0-9]\.\)20\(..\)/\1\2/' \
| tac >min_day.js

sqlite3 wechselrichter.db "select strftime('da[dx++]=\"%d.%m.%Y',dateTime) as date,\
    CAST (round(sum(ac1p+ac2p+ac3p)/4) AS INTEGER), \
    max(ac1p+ac2p+ac3p) \
 from measures\
 group by date \
 order by zeit desc" \
| awk -F '|' '{printf "%s|%s;%s\"\n",$1,$2,$3}' \
| sed -e 's/\([0-9][0-9]\.[0-9][0-9]\.\)20\(..\)/\1\2/' >days_hist.js
