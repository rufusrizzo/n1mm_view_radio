#!/bin/bash
#This script will just publish to your MQTT Broker to reset to NS.
#The display flickers if it doesn't have a value to show.
#Started by RileyC on 2/19/2024
#
for i in {1..6}
do
mosquitto_pub -h 127.0.0.1 -p 1883 -r -t n1mm_radio/stations/$i -m "                 "
mosquitto_pub -h 127.0.0.1 -p 1883 -r -t n1mm_radio/stations/${i}/time -m ""
done
sleep 6
for i in {1..6}
do
mosquitto_pub -h 127.0.0.1 -p 1883 -r -t n1mm_radio/stations/$i -m "    NS"
done
