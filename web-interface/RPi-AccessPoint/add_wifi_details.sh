#!/bin/bash

USER=$1
PASS=$2

echo "network={"	>> /etc/wpa_supplicant/wpa_supplicant.conf
echo "      ssid=\"$USER\""	 >> /etc/wpa_supplicant/wpa_supplicant.conf
echo "      psk=\"$PASS\""	>> /etc/wpa_supplicant/wpa_supplicant.conf
echo "}" 		>> /etc/wpa_supplicant/wpa_supplicant.conf

echo "Wifi Details added to wpa_supplicant.conf --- "
