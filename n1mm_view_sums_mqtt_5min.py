"""
n1mm_view Stats to MQTT
This program collects N1MM+ "Contact Info" broadcasts and saves data from the broadcasts
in MQTT every 5 minutes and keeps running
Started by Riley C and ChatGPT on 6/28/2024
"""

import sqlite3
import paho.mqtt.client as mqtt
import time
from datetime import datetime


# Path to your SQLite database file
database_file = '../n1mm_view/n1mm_view.db'

# MQTT configuration
MQTT_BROKER = '192.168.1.202'
MQTT_PORT = 1883
MQTT_TOPIC_BASE = 'n1mm_radio/stats'

def publish_mqtt(topic, message):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    client.publish(topic, message, retain=True)
    client.loop_stop()
    client.disconnect()

while True:
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Define the SQL query for operator stats
    operator_stats_query = """
    SELECT o.name AS operator_name, COUNT(*) AS count
    FROM qso_log q
    JOIN operator o ON q.operator_id = o.id
    GROUP BY o.name
    ORDER BY count DESC
    LIMIT 5;
    """

    # Define the SQL query for QSO summaries
    qso_summary_query = """
    SELECT
        SUM(CASE WHEN mode_id = 9 THEN 1 ELSE 0 END) AS count_9,
        SUM(CASE WHEN mode_id = 5 THEN 1 ELSE 0 END) AS count_5,
        SUM(CASE WHEN mode_id = 1 THEN 1 ELSE 0 END) AS count_1
    FROM qso_log
    """

    # Execute the QSO summary query
    cursor.execute(qso_summary_query)

    # Fetch the results
    qso_summary_results = cursor.fetchone()

    # Extract the results
    count_9, count_5, count_1 = qso_summary_results

    # Execute the operator stats query
    cursor.execute(operator_stats_query)

    # Fetch the top 5 operator results
    top_operators = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Output the results for debugging purposes
    current_datetime = datetime.now()
    print("#####################Run Time:", current_datetime)
    print(f"Data QSO Summary: {count_9}")
    print(f"Phone QSO Summary: {count_5}")
    print(f"CW QSO Summary: {count_1}")

    for i, (operator_name, count) in enumerate(top_operators, start=1):
        print(f"Top Operator {i}: {operator_name}, Count: {count}")

    # Publish the QSO summary results to separate MQTT topics
    publish_mqtt(f"{MQTT_TOPIC_BASE}/data_total", count_9)
    publish_mqtt(f"{MQTT_TOPIC_BASE}/phone_total", count_5)
    publish_mqtt(f"{MQTT_TOPIC_BASE}/cw_total", count_1)

    # Publish the top 5 operator stats to separate MQTT topics
    for i, (operator_name, count) in enumerate(top_operators, start=1):
        publish_mqtt(f"{MQTT_TOPIC_BASE}/top_op_{i}", f"{operator_name}: {count}")

    # Wait for 5 minutes before running the loop again
    time.sleep(300)

