#!/bin/bash
#Run in home folder

#Setup folder and utility
#https://www.raspberrypi.org/documentation/usage/webcams/
sudo apt-get install fswebcam
mkdir webcam
cd webcam

#Create script to run webcam capture
echo '#!/bin/bash ' > capture.sh
echo "" 							 >> capture.sh
echo 'DATE=$(date +"%Y-%m-%d_%H%M")' 				 >> capture.sh
echo 'raspistill -o /home/pi/webcam/$DATE.jpg'			 >> capture.sh
echo 'cp /home/pi/webcam/$DATE.jph /var/www/html/latest.jpg'	 >> capture.sh
chmod +x capture.sh

#Edit crontab
crontab -l > storedCrons
echo "*/5 * * * * /home/pi/webcam/capture.sh 2>&1" >> storedCrons
crontab storedCrons
rm 	storedCrons
