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
- [ ] Track time since last update, send Char to display
- [ ] Change band to show offline if no updates in 45min
- [ ] Document the esp8266 HW
- [ ] Document usage for others
- [ ] Document how to change the timezone in 2 places
- [ ] Generate n1mm_view images with Radio Data

