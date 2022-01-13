#!/usr/bin/python3
# inspired by
# https://arduinogetstarted.com/tutorials/arduino-temperature-humidity-sensor
# Testing use serial connection to arduino with setup
#
import serial
from datetime import datetime
import json
import requests

def getmeasurepoint():
    try:
        f = open("measure.conf", "r")
        return f.read()
    except:
        return "ds18b20"

def parse_data (s):
    unique=[]
    sensor_readings=[]
    cont=""
    readings = s.split(";")
    for reading in reversed(readings) :
      values = reading.split(":")
      if len(values) == 3 :
         if values[0] == "Sensor" :
            sensor_id =  values[1] 
            if sensor_id not in unique:
               unique.append(sensor_id)
               sensor_readings.append( cont + '{ "id" : "' + values[1] + '-' + place + '", "temp" : ' + values[2] + "}")
               cont = ","
    return sensor_readings

# "MAIN"
with open("config.json") as json_data_file:
    data = json.load(json_data_file)
API_ENDPOINT = data["API_ENDPOINT"]
DEVICE=data["DEVICE"]

lastplace = getmeasurepoint()
place = lastplace.replace("\n", "")

ser = serial.Serial(DEVICE, 9600, timeout=5)
ser.flushInput()
ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Start log " + place + ".log tid:" + ts)

ser_bytes = ser.read(200)
s: str = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")
temp_items=  parse_data(s)
dt =  datetime.now()
print ( datetime.timestamp(dt))
example = { "counter": '1234',
  "values": [
       { "id" : "id1-pi2", "temp" : 5.38 }
      ,{ "id" : "id2-pi2", "temp" : 28.75 }
      ,{ "id" : "id3-pi2", "temp" : 18.38 }
      ,{ "id" : "id4-pi2", "temp" : 20.7 }
  ]
    , "location": "pi-2"}

text = '{"counter" : "' + str( datetime.timestamp(dt)) +'",'
text = text + '"values" : [ '
for item in temp_items:
   text = text + item 
text=text + '], "location" : "pi-2"}'
print (text)
payload = json.loads(text)


with open("config.json") as json_data_file:
    data = json.load(json_data_file)
API_ENDPOINT = data["API_ENDPOINT"]
headers = {'Content-Type': 'application/json'}

r = requests.post(url=API_ENDPOINT, data=json.dumps(payload),headers=headers)
print(r.text + " status : " + str(r.status_code))

