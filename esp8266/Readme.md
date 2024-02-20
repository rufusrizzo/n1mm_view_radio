 I can barely hack together the things I need, but it works...

This display code is working now.
The ESP connects to a Defined WiFi network, and connects to a local NTP server.
It displays the local time, and UTC time with seconds.
Then is subscribes to 6 MQTT topics and displays what is there on different parts of the display.
The loader scripts will rename each station and assign it a Station number.
That station number will stay in the same location.
With a 20 character wide display, you're limited to what you can display.

##Parts I used
Depending how you make these, you can make them for about $10 per display.
I'll try to add a case and pictures when I'm done
###ESP8266
HiLetgo 5pcs Mini ESP8266 ESP-12F Mini NodeMCU Lua 4M Bytes WiFi Module with Pin Headers
https://www.amazon.com/gp/product/B073CQVFLK

###Display
I2C 2004 LCD Module | 20x04 LCD Screen Module 
https://www.amazon.com/gp/product/B0C1G9GBRZ

##Localization

Chage the values for your local network.
"<SSID>"  would be changed to "SuperAwesomeContestNet"
ETC...

const char* ssid = "<SSID>";
const char* password = "<Network Key>";
const char* mqtt_server = "<MQTT Server>";
NTPClient timeClient(ntpUDP, "<NTP SERVER>", -5 * 3600, 60000); // UTC offset for Eastern Time is -5 hours (-5 * 3600 seconds)


##Arduino IDE
I've added so many libraries to my Arduino IDE, make sure you add everything in the include statements at the top of the file.
