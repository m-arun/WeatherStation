import requests
import json
import time
import os
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler
import sys






influxClient = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', 'climo')
influxClient_combined = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', 'air_climo')
fileName = "./logs/log.csv"

properties = ["SENS_LIGHT", "SENS_AIR_PRESSURE", "SENS_TEMPERATURE", "SENS_CARBON_DIOXIDE",
"SENS_RELATIVE_HUMIDITY", "SENS_SOUND", "SENS_NITRIC_OXIDE", "SENS_ULTRA_VIOLET", "SENS_PM2P5",
"SENS_PM10", "SENS_NITROGEN_DIOXIDE", "SENS_CARBON_MONOXIDE", "SENS_SULPHUR_DIOXIDE", "SENS_OZONE"]

aqi_sub = ["SENS_PM2P5", "SENS_PM10", "SENS_NITROGEN_DIOXIDE", "SENS_CARBON_MONOXIDE", "SENS_SULPHUR_DIOXIDE", "SENS_OZONE"]





bosch_thing_headers = ""
aqi_url = ""
poll_url = ""
def authorize():
    global bosch_thing_headers, aqi_url, poll_url
    bosch_auth_url = "http://52.28.187.167/services/api/v1/users/login"
    bosch_auth_headers = {"Content-Type":"application/json", "Accept":"application/json", "api_key":"apiKey"}
    bosch_auth_payload = {"password":"Q2xpbW9AOTAz", "username":"SUlTQ19CQU5HQUxPUkU="}
    auth_res = requests.post(url = bosch_auth_url, headers = bosch_auth_headers, data = json.dumps(bosch_auth_payload))
    print("Authorizing")
    print(auth_res)
    authToken = auth_res.json()["authToken"]
    OrgKey = auth_res.json()["OrgKey"]
    bosch_thing_url = "http://52.28.187.167/services/api/v1/getAllthings"
    bosch_thing_headers = {"Accept":"application/json", "api_key":"apiKey", "Authorization":authToken, "X-OrganizationKey":OrgKey}
    thing_res = requests.get(url = bosch_thing_url, headers = bosch_thing_headers)
    thingKey = thing_res.json()["result"][0]["thingKey"]
    print(thingKey)
    aqi_url = "http://52.28.187.167/services/api/v1/thing/" + thingKey + "/aqi/{propertyKey}/1/INDIA"
    poll_url = "http://52.28.187.167/services/api/v1/property/" + thingKey + "/{propertyKey}/1m"


sens_data = {}
for key in properties:
    sens_data[key] = 0.0

aqi = {}
for key in aqi_sub:
    aqi[key] = 0.0

f = open(fileName,'a')
f.write("timestamp")
f.write(",")
for key in sens_data:
    f.write(key)
    f.write(",")
f.write("\n")

scheduler = BackgroundScheduler()
scheduler.add_job(authorize, 'interval', hours=10)
scheduler.start()

authorize()
series = []
while True:
    f = open(fileName,'a')
    for p in properties:
        try:
            r = requests.get(url=poll_url.replace("{propertyKey}", p), headers = bosch_thing_headers)
            if(r.json()["result"]["values"] is not None):
                sens_data[p] = r.json()["result"]["values"][0]["value"]
            else:
                pass
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    for p in aqi_sub:
        try:
            r = requests.get(url=aqi_url.replace("{propertyKey}", p), headers = bosch_thing_headers)
            if(r.json()["result"][0]["values"] is not None):
                aqi[p] = r.json()["result"][0]["values"]
            else:
                pass
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    epochTime = time.time()

    f.write(str(epochTime) + ",")
    epochTime_ns = int(time.time()) * 1000000000
    series = []
    for keys in sens_data :
        f.write('{0:.3f}'.format(sens_data[keys]))
        f.write(",")
        pointValues = {
            "time": epochTime_ns,
            "measurement": keys,
            'fields': {
                'value': sens_data[keys],
            },
            'tags': {
                "sensorName": keys,
            },
        }
        series.append(pointValues)


    for keys in aqi :
        pointValues = {
            "time": epochTime_ns,
            "measurement": "AQI_"+keys,
            'fields': {
                'value': aqi[keys],
            },
            'tags': {
                "sensorName": "AQI_"+keys,
            },
        }
        series.append(pointValues)
    try:
        influxClient.write_points(series, time_precision='n')
        influxClient_combined.write_points(series, time_precision='n')
    except Exception as e:
        print(e)
    print(series)

    f.write("\n")
    f.close()
    print("\n")
    time.sleep(60)


    
data = {}
data["reference"] = "a"
data["confirmed"] = False
data["fport"] = 1
data["data"] = json.dumps(sens_data)
http_dict = json.dumps(data)
#print(sens_data)
