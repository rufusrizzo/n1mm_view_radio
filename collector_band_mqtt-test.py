import socket
import json
import xml.etree.ElementTree as ET
import paho.mqtt.client as mqtt

# Define MQTT broker settings
broker_address = "127.0.0.1"
broker_port = 1883
topic_prefix = "n1mm_radio/stations/"
topic = "n1mm_radio/stations/6"

# Read config file
with open("n1mm_stations.json", "r") as f:
    config = json.load(f)

# Define replacements from config file
replacements = config.get("replacements", {})

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect

# Connect to MQTT broker
client.connect(broker_address, broker_port, 60)

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

    # Print the value
    print("Station Name:", sn, "| Operator:", oc, "| Frequency:", freq, "| Band:", band)
    mfreq = int(str(freq)[:-2])
    topic = topic_prefix + disp_pos

    # Publish data to MQTT broker
    client.publish(topic, f"{msn},B:{band}")
    #Test data to see on the little display
    client.publish(topic_prefix + "2", f"VCE,B:20")
    client.publish(topic_prefix + "3", f"CW,B:80")
    client.publish(topic_prefix + "4", f"GTA,B:10")
    client.publish(topic_prefix + "5", f"VHF,B:2")
    client.publish(topic_prefix + "6", f"APR,B:40")
    # Unsetting the band
    band = "null"

# Run the MQTT client loop in a non-blocking manner
client.loop_start()



