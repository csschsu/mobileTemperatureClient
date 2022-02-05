#!/usr/bin/python3
# inspired by
# https://arduinogetstarted.com/tutorials/arduino-temperature-humidity-sensor
# Testing use serial connection to arduino with setup
# read from arduino onewire for multiple ds18b20 temperature sensors and post a
# data file to a mobileTemperatureServer API
#
# This shows how the file should look when sent
# example_file_data = {"counter": "1234",
#                     "values": [
#                         {"id": "id1-pi2", "temp": 5.38},
#                         {"id": "id2-pi2", "temp": 28.75},
#                         {"id": "id3-pi2", "temp": 18.38},
#                         {"id": "id4-pi2", "temp": 20.7}
#                     ],
#                     "location": "pi-2"}
#

import json
import datetime
import requests
import serial
from check import temp_value


class DataError(Exception):
    pass


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
                    try:
                        temp_value(values[2])  # raises ValueError
                        unique.append(sensor_id)
                        sensor_readings.append(
                            cont + '{ "id" : "' + values[1] + '-' + SENSOR + '", "temp" : ' + values[2] + "}")
                        cont = ","
                    except ValueError:
                        print("sensor_id : " + sensor_id + " has invalid temperature : " + values[2])
    if sensor_readings == []:
        raise DataError
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
    BUFFERSIZE = data["BUFFERSIZE"]
    READSPEED = data["READSPEED"]
    TIMEOUT = data["TIMEOUT"]

ser = serial.Serial(DEVICE, READSPEED, timeout=TIMEOUT)
ser.flushInput()

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
s = ""

try:
    ser_bytes = ser.read(BUFFERSIZE)
    s: str = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")
#    print(s)

    temp_items = parse_data()

    text = '{"counter" : 1234 ,'
    text = text + '"values" : [ '
    for item in temp_items:
        text = text + item
    text = text + '], "location" : "' + LOCATION + '"}'
    print(dt + " " + text)

    if FILENAME != "":
        f = open(FILENAME, "w")
        f.write(text)
        f.close()

    if API_ENDPOINT != "":
        payload = json.loads(text)
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url=API_ENDPOINT, data=json.dumps(payload), headers=headers)
        print(r.text)

except UnicodeError:
    print("Error reading arduino'")

except DataError:
    print(dt + "Error in arduino data, start '")
    print(s)
    print("'end")

exit()
