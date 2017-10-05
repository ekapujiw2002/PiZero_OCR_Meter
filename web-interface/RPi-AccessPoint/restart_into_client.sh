#!/bin/bash

#Assumes there are pre-configured interface files
#As following: 
#interface-client for a client usage of the PI (normal usage)
#interface-host for a server usage of the PI (act as access point)
cp /etc/network/interfaces-client /etc/network/interface

shutdown -r now
