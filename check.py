#!/usr/bin/python3
import config


class DataError(Exception):
    pass


def temp_value(s):
    if len(s) != 5:
        raise DataError
    if s[2] != ".":
        raise DataError
    for char in s:
        if char.isdigit() is False and char != ".":
            raise DataError
    return

def id_value(s):
    if len(s) > 3:
        raise DataError
    for char in s:
        if char.isnumeric() is False:
            raise DataError
    return


def pressure_id(s):
    if not s.startswith("Temperature"):
        raise DataError
    return


def pressure_value(s):
    # 900.00 - 1100.00
    if len(s) < 6 or len(s) > 7:
        raise DataError
    items = s.split('.')
    if len(items[1]) != 2:
        raise DataError
    for char in s:
        if char.isdigit() is False and char != ".":
            raise DataError
    return


def humidity_value(s):
    # 35.00
    if len(s) != 5:
        raise DataError
    if s[2] != ".":
        raise DataError
    for char in s:
        if char.isdigit() is False and char != ".":
            raise DataError
    return


def sensor_id(s):
    if not s == ("Sensor"):
        raise DataError
    return


def humidity_id(s):
    if not s.startswith("Humidity"):
        raise DataError
    return


def start_id(s):
    if not s.startswith("Start"):
        raise DataError
    return


def end_id(s):
    if not s.endswith("End"):
        raise DataError
    return


conf = config.Config()


def _parse(buff):
    unique = []
    sensor_readings = []
    cont = ""
    readings = buff.split(";")
    for reading in reversed(readings):
        values = reading.split(":")
        if len(values) == 3:
            if values[0] == "Sensor":
                sensor_id = values[1]
                if sensor_id not in unique:
                    try:
                        temp_value(values[2])  # raises DataError
                        unique.append(sensor_id)
                        sensor_readings.append(
                            cont + '{ "id" : "' + values[1] + '-' + conf.SENSOR + '", "temp" : ' + values[2] + "}")
                        cont = ","
                    except DataError:
                        print("sensor_id : " + sensor_id + " has invalid temperature : " + values[2])
    if not sensor_readings:
        raise DataError
    return sensor_readings


def ds18b20_sensors_parse(s):
    # Arduino message @see test/1.ok

    it = []
    lines = s.split('---')
    if len(lines) < 2: raise DataError
    if not lines[1].startswith("Sensor"): raise DataError
    if not lines[1].endswith(";"): raise DataError

    sns = lines[1][0:len(lines[1])-1]       # remove last ";"
    sensors = sns.split(';')
    filler = ""
    for sensor in sensors:
        items = sensor.split(':')
        if len(items) != 3 : raise DataError  # not Sensor:X:YY.ZZ
        sensor_id(items[0])
        id_value(items[1])
        temp_value(items[2])
        it.append( filler + '{ "id" :' + items[1] + ', "temp" :' + items[2] + '}'  )
        filler = ","
    return it


def dht21_bmp280_sensors_parse(s):
    items = s.split(':')
    if len(items) < 9: raise DataError
    if items[1] != "Start": raise DataError
    if items[2] != "Pressure": raise DataError
    pressure_value(items[3])
    if items[4] != "Humidity": raise DataError
    humidity_value(items[5])
    if items[6] != "Temperature": raise DataError
    temp_value(items[7])
    if items[8] != "End": raise DataError

    it = ['{' +
          '"' + items[2] + '" :' + items[3] + ',' +
          '"' + items[4] + '" :' + items[5] + ',' +
          '"' + items[6] + '" :' + items[7] +
          '}']

    return it


def create_response(items):
    # example = {"counter": "1234",
    #                     "values": [
    #                         {"id": "id1-pi2", "temp": 5.38},
    #                         {"id": "id2-pi2", "temp": 28.75},
    #                         {"id": "id3-pi2", "temp": 18.38},
    #                         {"id": "id4-pi2", "temp": 20.7}
    #                     ],
    #                     "location": "pi-2"}
    text = '{"counter" : 1234 ,'
    text = text + '"values" : [ '
    for item in items:
        text = text + item
    text = text + '], "location" : "' + conf.LOCATION + '"}'
    return text
