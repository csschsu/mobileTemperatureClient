#!/usr/bin/python3
# Serial read of Arduino one-wire implementation of the ds18b20 temperature sensor see (pgm) ds18b20.ino
# Sending temperature data to file/API
#

import os
import json
import datetime
import requests
import serial
from config import Config
from check import DataError
from check import create_response
from check import ds18b20_sensors_parse

conf = Config()
buff = ""


def read_serial():
    ser = serial.Serial(conf.DEVICE, conf.READSPEED, timeout=conf.TIMEOUT)
    ser.flushInput()
    ser_bytes = ser.read(conf.BUFFERSIZE)
    return ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")


def create_file():
    f = open(conf.FILENAME, "w")
    f.write(text)
    f.close()


def send_to_api():
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=conf.API_ENDPOINT, data=text, headers=headers)
    print(r.text)


#
# "MAIN"
#

try:

    buff = read_serial()
    items = ds18b20_sensors_parse(buff)
    if conf.PRINTMSG == "Y": print(buff)

    text = create_response(items)
    if conf.PRINTMSG == "Y": print(text)

    if conf.FILENAME != "":
        create_file()

    if conf.API_ENDPOINT != "":
        send_to_api()

except UnicodeError:
    print("Error reading arduino'")

except json.decoder.JSONDecodeError as e:
    print("Error reading arduino, not connected ?'")
    print(e)
except serial.serialutil.SerialException:
    print("Error reading arduino, not connected ?'")

except DataError:
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Error in arduino data, data: ")
    print(buff)

except NewConnectionError as e:
    os.system('systemctl reboot -i')

exit()
