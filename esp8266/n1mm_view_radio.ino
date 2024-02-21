#include <PubSubClient.h>
#include <LiquidCrystal_I2C.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ESP8266WiFi.h>

// Define LCD parameters
int lcdColumns = 20;
int lcdRows = 4;
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);

// Define Wi-Fi credentials
const char* ssid = "<SSID>";
const char* password = "<Network Key>";

// Define MQTT parameters
const char* mqtt_server = "<MQTT Server IP>";
const int mqtt_port = 1883;
const char* mqtt_topic = "n1mm_radio/stations";
const int num_topics = 6;
const char* mqtt_topics[] = {
  "n1mm_radio/stations/1",
  "n1mm_radio/stations/2",
  "n1mm_radio/stations/3",
  "n1mm_radio/stations/4",
  "n1mm_radio/stations/5",
  "n1mm_radio/stations/6"
};
String receivedMessages[num_topics];

// Define NTP parameters
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "<NTP Server>", -5 * 3600, 60000); // UTC offset for Eastern Time is -5 hours (-5 * 3600 seconds)

// Wi-Fi client and MQTT client
WiFiClient espClient;
PubSubClient client(espClient);

// Function prototypes
void reconnect();
void callback(char* topic, byte* payload, unsigned int length);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  // Print WiFi status
  Serial.println();
  Serial.print("WiFi connected, IP address: ");
  Serial.println(WiFi.localIP());

  // Initialize LCD
  lcd.init();
  lcd.backlight();
  lcd.clear();

  // Initialize NTP client
  timeClient.begin();

  // Set MQTT server and callback function
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  // Attempt to connect to Wi-Fi and MQTT
  reconnect();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  // Handle MQTT messages
  for (int i = 0; i < num_topics; i++) {
    lcd.setCursor(i % 2 * 11, i / 2 + 1);
    lcd.print(receivedMessages[i]);
  }

  // Update NTP time
  timeClient.update();
  
  // Display Eastern time
  lcd.setCursor(0, 0);
  lcd.print("L-");
  lcd.print(timeClient.getFormattedTime().substring(0, 8)); // Display time HH:MM

  // Display UTC time
  lcd.setCursor(13, 0);
  lcd.print("U-");
  //You will have to manually adjust the offset for your timezone and Daylight savings.
  int offset = 5; // UTC offset for Eastern Time is 5 hours
  int utcHour = (timeClient.getHours() + offset + 24) % 24; // Adjust for offset and handle negative values
  if (utcHour < 10) {
    lcd.print("0"); // Add leading zero if needed
  }
  lcd.print(utcHour);
  lcd.print(":");
  if (timeClient.getMinutes() < 10) {
    lcd.print("0"); // Add leading zero if needed
  }
  lcd.print(timeClient.getMinutes());
  
  delay(1000); // Adjust delay as needed
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Callback function to handle received messages
  Serial.print("Message received on topic: ");
  Serial.println(topic);
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.print("Message: ");
  Serial.println(message);
  // Store the received message in the receivedMessages array
  for (int i = 0; i < num_topics; i++) {
    if (strcmp(topic, mqtt_topics[i]) == 0) {
      receivedMessages[i] = message;
      break;
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      for (int i = 0; i < num_topics; i++) {
        client.subscribe(mqtt_topics[i]);
      }
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      Serial.println();
      Serial.print("WiFi connected, IP address: ");
      Serial.println(WiFi.localIP());

      lcd.clear();
      lcd.setCursor(2, 0);
      lcd.print("Server");
      lcd.setCursor(2, 1);
      lcd.print("DOWN");
      lcd.setCursor(2, 2);
      lcd.print("IP:");
      lcd.setCursor(2, 3);
      lcd.print(WiFi.localIP());

      delay(5000);
      lcd.clear();
    }
  }
}

