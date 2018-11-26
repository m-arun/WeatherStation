#!/usr/bin/ python

import paho.mqtt.client as mqtt
import json
import time
import serial

MQTT_HOST = "gateways.rbccps.org"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 145

MQTT_TOPIC = "e-city/weatherstation"
MQTT_USERNAME = "loraserver"
MQTT_PASSWORD = "loraserver"

# Define on_publish event function
def on_publish(client, userdata, mid):
    print ("Message Published...")

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload) 
    client.disconnect() 

# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function

mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


def getMAC(interface='eth0'):
# Return the MAC address of the specified interface
    macId = ""
    try:
        macId = open('/sys/class/net/%s/address' %interface).read()
    except:
        macId = "00:00:00:00:00:00"
    return macId.replace(":","")

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
counter=0

while 1:
    values={}
    x=ser.readline()
    if x:  
        measures=x.split(",")
        values['windSpeed']=float(measures[0])
        values['windDirection']=int(measures[1])
        values['rainfall']=float(measures[2][:-2])
        values['id']=getMAC('eth0')[:-1]
        values['timestamp']=time.time()
        data=json.dumps(values)
        print (data)
        mqttc.publish(MQTT_TOPIC, data)



