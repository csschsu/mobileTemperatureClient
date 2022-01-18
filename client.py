#!/usr/bin/python3
# inspired by
# https://arduinogetstarted.com/tutorials/arduino-temperature-humidity-sensor
# Testing use serial connection to arduino with setup
# read from arduino onewire for multiple ds18b20 temperature sensors and post a
# data file to a mobileTemperatureServer API
#

import json
from datetime import datetime

import requests
import serial


def parse_data():
    unique = []
    sensor_readings = []
    cont = ""
    readings = s.split(";")
    for reading in reversed(readings):
        values = reading.split(":")
        if len(values) == 3:
            if values[0] == "Sensor":
                sensor_id = values[1]
                if sensor_id not in unique:
                    unique.append(sensor_id)
                    sensor_readings.append(
                        cont + '{ "id" : "' + values[1] + '-' + SENSOR + '", "temp" : ' + values[2] + "}")
                    cont = ","
    return sensor_readings


#
# "MAIN"
#

with open("setup.json") as json_data_file:
    data = json.load(json_data_file)
    API_ENDPOINT = data["API_ENDPOINT"]
    DEVICE = data["DEVICE"]
    FILENAME = data["FILENAME"]
    LOCATION = data["LOCATION"]
    SENSOR = data["SENSOR"]

ser = serial.Serial(DEVICE, 9600, timeout=5)
ser.flushInput()
ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Start log " + LOCATION + ".log tid:" + ts)

ser_bytes = ser.read(200)
s: str = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")
temp_items = parse_data()
dt = datetime.now()

text = '{"counter" : "' + str(datetime.timestamp(dt)) + '",'
text = text + '"values" : [ '
for item in temp_items:
    text = text + item
text = text + '], "location" : "' + LOCATION + '"}'

if FILENAME != "":
    f = open(FILENAME, "w")
    f.write(text)
    f.close()

else:
    payload = json.loads(text)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=API_ENDPOINT, data=json.dumps(payload), headers=headers)
    print(r.text + " status : " + str(r.status_code))

exit()

# This shows how the file should look when sent
example_file_data = {"counter": "1234",
                     "values": [
                         {"id": "id1-pi2", "temp": 5.38},
                         {"id": "id2-pi2", "temp": 28.75},
                         {"id": "id3-pi2", "temp": 18.38},
                         {"id": "id4-pi2", "temp": 20.7}
                     ],
                     "location": "pi-2"}
