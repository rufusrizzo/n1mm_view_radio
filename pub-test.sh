#!/bin/bash
#This script will just publish to your MQTT Broker to test your display
#Started by RileyC on 2/19/2024
#
for x in {1..99}
do
for i in {1..6}
do
# Define the string of numbers
#160 is broken on the display
numbers="160 80m 40m 30m 20m 17m 15m 10m 06m"
# Convert the string into an array
IFS=' ' read -r -a numbers_array <<< "$numbers"
# Get the length of the array
length=${#numbers_array[@]}
# Generate a random index within the range of the array length
random_index=$((RANDOM % length))
# Get the randomly selected number
random_number=${numbers_array[random_index]}



# Display the randomly selected number and publish to the MQTT broker
#Change your local MQTT info below
mosquitto_pub -h 127.0.0.1 -p 1883 -r -t n1mm_radio/stations/$i -m "DIG,B:${random_number}" 
echo "Randomly selected number: $random_number"
done
sleep 1
done
