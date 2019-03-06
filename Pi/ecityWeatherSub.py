#!/usr/bin/ python

import paho.mqtt.client as mqtt
import sys
import json
import requests


# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("e-city/weatherstation")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

        decodedData = json.loads(msg.payload)
        print(decodedData["windSpeed"])
        print(decodedData["windDirection"])
        print(decodedData["rainfall"])
	print ''

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("loraserver","loraserver")

client.connect("gateways.rbccps.org", 1883, 45)
client.loop_forever()


