#!/bin/bash
#This script will act like n1mm sending radio data over the network.
#You should just need netcat
#
#Started by RileyC on 2/20/2024
#
#date +'%Y-%m-%d %H:%M:%S'

#Define your n1mm collector host and port
def_host=127.0.0.1
def_port=12060

HOST=${2:-$def_host}
PORT=${3:-$def_port}

#This will get a list of all the local xml files and shuffle them, then play them to the collector
for FILE in `cat calls.txt | shuf`

	do
	DDATEE=`date +'%Y-%m-%d %H:%M:%S'`
	random_hex=$(head -c 17 /dev/urandom | xxd -p | tr -d '\n' | cut -c 1-33)
	cat n1mm_contact_template.xml | sed "s/REMOTECALLL/$FILE/g" | sed "s/TIMESTAMPPP/$DDATEE/g" | sed "s/IDDDD/$random_hex/g" | nc -u -w1 $HOST $PORT
	
#	sleep 5
done

