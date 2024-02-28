I like the n1mm_view project, but I wanted to add Radio info to it.

This will listen on a UDP port and do stuff with the N1MM data. 
My goal is to display multiple stations Band status on a small display during field day.
If I can I'd like to also display a graphic on a n1mm_view page to see the stations's band status.


#ToDo
- [x] Listen on a UDP Port for N1MM Radio information
- [x] Format and print to the terminal
- [x] Post the data to MQTT broker
- [x] Get a ESP8266 Reading the data from the MQTT Broker
- [ ] MQTT broker settings and howto
- [X] Post the data to multiple MQTT Topics, one for each OpStation
- [ ] Add an option to limit the display to 3 stations, and show band plan
- [x] Track time since last update, send Char to display
- [X] Change band to show offline if no updates in 45min
- [ ] Document the esp8266 HW
- [ ] Document usage for others
- [ ] Document how to change the timezone in 2 places
- [x] Generate n1mm_view images with Radio Data
- [ ] Document how to copy the image to the n1mm_view image dir
- [X] Add offline to the image topic
- [ ] Add adafruit 16x32 LED matrix code
- [ ] Add adafruit 16x32 LED matrix HW docs

