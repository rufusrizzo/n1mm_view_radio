#!/usr/bin/python3
"""
n1mm_view radio
This program collects N1MM+ "Radio Info" broadcasts and saves data from the broadcasts
in MQTT 
"""

import socket
import json
import xml.etree.ElementTree as ET
import paho.mqtt.client as mqtt
import time

# This sets how often the script will check for offline stations.
interval = 300

# Define MQTT broker settings
broker_address = "127.0.0.1"
broker_port = 1883
topic_prefix = "n1mm_radio/stations/"

start_time = time.time()


# Dictionary to store time_station variables
time_stations = {i: None for i in range(1, 7)}

# Read config file
with open("n1mm_stations.json", "r") as f:
    config = json.load(f)

# Define replacements from config file
replacements = config.get("replacements", {})

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    for i in range(1, 7):
        client.subscribe(topic_prefix + str(i) + "/time")

# Callback function for MQTT message received
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    station_number = int(topic.split("/")[-2])
    time_stations[station_number] = payload

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker_address, broker_port, 60)

# Start the MQTT client loop
client.loop_start()

port = 12061
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print("waiting on port:", port)

while True:
    data, addr = s.recvfrom(1024)
    # Parse the XML string
    root = ET.fromstring(data)
    # Find the Freq element and extract its value
    freq = int(root.find('Freq').text)
    sn = root.find('StationName').text
    oc = root.find('OpCall').text

    # Get replacement values from config file if available
    replacement = replacements.get(sn, {})
    msn = replacement.get("msn", sn)
    disp_pos = replacement.get("disp_pos", sn)

    #Setting the band based on Frequency
    if 100000 < freq < 300000:
       band=("160m")
    if 320000 < freq < 400000:
       band=("80m")
    if 533000 < freq < 550000:
       band=("80m")
    if 700000 < freq < 800000:
       band=("40m")
    if 1000000 < freq < 1100000:
       band=("30m")
    if 1300000 < freq < 1500000:
       band=("20m")
    if 1800000 < freq < 1820000:
       band=("17m")
    if 2000000 < freq < 2300000:
       band=("15m")
    if 2400000 < freq < 2600000:
       band=("12m")
    if 2700000 < freq < 3000000:
       band=("10m")
    if 5000000 < freq < 5500000:
       band=("6m")
    if 14400000 < freq < 14800000:
       band=("2m")
    if 21900000 < freq < 22500000:
       band=("220")
    if 42000000 < freq < 45000000:
       band=("70c")
    if 90200000 < freq < 92800000:
       band=("33c")
    if 124000000 < freq < 130000000:
       band=("23c")
    if freq == 0:
        band=("NA")

    # Get the current time
    current_time_hr = time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())

    # Print the value
    print(current_time_hr, "| Station Name:", sn, "| Xlated Name:", msn, "| Operator:", oc, "| Frequency:", freq, "| Band:", band)
    mfreq = int(str(freq)[:-2])
    topic = topic_prefix + disp_pos

    # Publish time to MQTT broker
    client.publish(topic_prefix + f"{disp_pos}/time", time.time(), retain=True)

    # Publish data to MQTT broker
    client.publish(topic, f"{msn},B:{band}", retain=True)

    # Checking the checkin time for each station
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= interval:
        for station_number, time_station in time_stations.items():
            if time_station is not None:
                time_station_float = float(time_station)
                if current_time - time_station_float > interval + 5:
                    print(f"Station {station_number} appears offline")
                    client.publish(f"n1mm_radio/stations/{station_number}", " OFFLINE ", retain=True)
        # Reset the start time for the next interval
        start_time = current_time

    # Unsetting the band
    band = "null"

