#!/usr/bin/env python3

import paho.mqtt.subscribe as subscribe
import yaml
from motor_control * 

def subscribe()

	for i in range(1):
		print("Waiting for a message from the broker...")
		msg = subscribe.simple(dict["Variables"]["Topic"],hostname=dict["Variables"]["Broker_IP"])
		print(msg.payload + " recieved.")
	Find_Lock(msg.payload, dict, Gantry_Pins)
	GPIO.cleanup()




