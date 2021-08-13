#!/bin/sh
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

while :;
do
	echo -n 'Checking gpsd... '
	if ! timeout 5s gpspipe -w -n 5 > /dev/null
	then
		echo 'FAIL! Restarting...'
		killall gpsd
		/etc/init.d/gpsd restart
	else
		echo 'OK.'
	fi
	sleep 60
done

