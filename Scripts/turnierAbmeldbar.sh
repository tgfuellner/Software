#!/bin/bash

URL='http://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/tournamentCalendarDetail?circuit=2015_CoBa_BTTR&federation=ByTTV&tournament=177287'

while [ 1 ]
do

	wget -q -O - "$URL" | grep '0 freie Plätze'

	if [ $? -eq 1 ]
	then
		echo "*** Sending Email ***"

		./send.py -s "Turnier: Erding Mi. 22.04. 20:00" -b "Bitte anmelden"
	fi

	sleep 900
done
