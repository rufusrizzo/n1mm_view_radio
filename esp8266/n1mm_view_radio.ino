
#ifdef ESP8266
#include <ESP8266WiFi.h>
#else
#include <WiFi.h>
#endif
#include <time.h>
#include <PubSubClient.h>
#include <LiquidCrystal_I2C.h>

int lcdColumns = 20;
int lcdRows = 4;

LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);  



const char* ssid = "wless-guest";
const char* password = "abc123def456!";

const char* NTP_SERVER = "192.168.1.123";
const char* TZ_INFO    = "EST5EDT";  // enter your time zone (https://remotemonitoringsystems.ca/time-zone-abbreviations.php)
const char* TZ_INFO2    = "UTC"; 

tm timeinfo;
time_t now;
long unsigned lastNTPtime;
unsigned long lastEntryTime;

// MQTT broker
const char* mqtt_server = "192.168.1.202";
const int mqtt_port = 1883; // Default MQTT port
//const char* mqtt_username = "YourMQTTUsername";
//const char* mqtt_password = "YourMQTTPassword";
// MQTT topic to subscribe to
const char* mqtt_topic = "n1mm_radio/stations";

WiFiClient espClient;
PubSubClient client(espClient);

// Variable to store the received message
String receivedMessage = "";



void setup() {
  Serial.begin(115200);
  Serial.println("\n\nNTP Time Test\n");
  WiFi.begin(ssid, password);




  int counter = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(200);
    if (++counter > 100) ESP.restart();
    Serial.print ( "." );
  // initialize LCD
  lcd.init();
  // turn on LCD backlight                      
  lcd.backlight();
  lcd.clear();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  // Connect to MQTT broker
  reconnect();

  }
  Serial.println("\n\nWiFi connected\n\n");

  configTime(0, 0, NTP_SERVER);
  // See https://github.com/nayarsystems/posix_tz_db/blob/master/zones.csv for Timezone codes for your region
  setenv("TZ", TZ_INFO, 1);

  if (getNTPtime(10)) {  // wait up to 10sec to sync
  } else {
    Serial.println("Time not set");
    ESP.restart();
  }
  showTime(timeinfo);
  lastNTPtime = time(&now);
  lastEntryTime = millis();
}


void loop() {
  //MQTT Connect
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // getTimeReducedTraffic(3600);
  getNTPtime(10);
  showTime(timeinfo);
  delay(1000);
  lcd.setCursor(0,1);
  lcd.print(receivedMessage);
}

bool getNTPtime(int sec) {

  {
    uint32_t start = millis();
    do {
      time(&now);
      localtime_r(&now, &timeinfo);
      Serial.print(".");
      delay(10);
    } while (((millis() - start) <= (1000 * sec)) && (timeinfo.tm_year < (2016 - 1900)));
    if (timeinfo.tm_year <= (2016 - 1900)) return false;  // the NTP call was not successful
    Serial.print("now ");  Serial.println(now);
    char time_output[30];
    strftime(time_output, 30, "%a  %d-%m-%y %T", localtime(&now));
    Serial.println(time_output);
    Serial.println();
  }
  return true;


}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on topic: ");
  Serial.println(topic);

  Serial.print("Message: ");
  receivedMessage = "";

  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    receivedMessage += (char)payload[i];
    lcd.clear();

  }
  Serial.println();

}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}


void showTime(tm localTime) {
  Serial.print(localTime.tm_mon + 1);
  Serial.print('/');
  Serial.print(localTime.tm_mday);
  Serial.print('/');
  Serial.print(localTime.tm_year - 100);
  Serial.print('-');
  Serial.print(localTime.tm_hour);
  Serial.print(':');
  Serial.print(localTime.tm_min);
  Serial.print(':');
  Serial.print(localTime.tm_sec);
  //Printing Date and Time to LCD
  lcd.setCursor(0,0);
  lcd.print(localTime.tm_mon + 1);
  lcd.setCursor(2,0);
  lcd.print('/');
  lcd.setCursor(3,0);
  lcd.print(localTime.tm_mday);
  lcd.setCursor(5,0);
  lcd.print('/');
  lcd.setCursor(6,0);
  lcd.print(localTime.tm_year - 100);
  lcd.setCursor(8,0);
  lcd.print(' ');
  lcd.setCursor(9,0);
  lcd.print(localTime.tm_hour);
  lcd.setCursor(11,0);
  lcd.print(':');
  lcd.setCursor(12,0);
  lcd.print(localTime.tm_min);
  lcd.setCursor(14,0);
  lcd.print('U');
  lcd.setCursor(15,0);
  lcd.print(localTime.tm_hour + 5);
  lcd.setCursor(17,0);
  lcd.print(':');
  lcd.setCursor(18,0);
  lcd.print(localTime.tm_min);


}


