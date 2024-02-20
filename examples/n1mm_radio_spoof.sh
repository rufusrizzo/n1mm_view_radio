#!/bin/bash
#This script will act like n1mm sending radio data over the network.
#You should just need netcat
#
#Started by RileyC on 2/20/2024
#

#Define your n1mm collector host and port
def_host=127.0.0.1
def_port=12061

HOST=${2:-$def_host}
PORT=${3:-$def_port}

#This will get a list of all the local xml files and shuffle them, then play them to the collector
for FILE in `ls -ltr *.xml | awk '{print $9}' | shuf`

	do
	cat $FILE | nc -u -w1 $HOST $PORT
	
	sleep 5
done

