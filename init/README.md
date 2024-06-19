#Copy the unit file in place

sudo cp n1mm_view_radio.service /usr/lib/systemd/system

#Change the user and directory based on your local system in the file you copied

#Enable the service

sudo systemctl daemon-reload
sudo systemctl enable n1mm_view_radio

#Start the service
sudo service n1mm_view_radio restart ; sudo service n1mm_view_radio status

