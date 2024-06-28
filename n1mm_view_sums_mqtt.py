import sqlite3
import paho.mqtt.client as mqtt

# Path to your SQLite database file
database_file = '../n1mm_view/n1mm_view.db'

# MQTT configuration
MQTT_BROKER = '192.168.1.202'
MQTT_PORT = 1883
MQTT_TOPIC_BASE = 'n1mm_radio/stats'

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Define the SQL query
query = """
SELECT
    SUM(CASE WHEN mode_id = 9 THEN 1 ELSE 0 END) AS count_9,
    SUM(CASE WHEN mode_id = 5 THEN 1 ELSE 0 END) AS count_5,
    SUM(CASE WHEN mode_id = 1 THEN 1 ELSE 0 END) AS count_1
FROM qso_log
"""

# Execute the query
cursor.execute(query)

# Fetch the results
results = cursor.fetchone()

# Close the database connection
conn.close()

# Extract the results
count_9, count_5, count_1 = results

# Output the results for debugging purposes
print(f"Data QSO Summary: {count_9}")
print(f"Phone QSO Summary: {count_5}")
print(f"CW QSO Summary: {count_1}")

# Function to publish MQTT messages
def publish_mqtt(topic, message):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    client.publish(topic, message, retain=True)
    client.loop_stop()
    client.disconnect()

# Publish the results to separate MQTT topics
publish_mqtt(f"{MQTT_TOPIC_BASE}/data_total", count_9)
publish_mqtt(f"{MQTT_TOPIC_BASE}/phone_total", count_5)
publish_mqtt(f"{MQTT_TOPIC_BASE}/cw_total", count_1)

