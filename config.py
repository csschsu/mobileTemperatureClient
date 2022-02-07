import json


class Config:

    TESTDATA: object

    def __init__(self):
        with open("setup.json") as json_data_file:
            data = json.load(json_data_file)
            self.API_ENDPOINT = data["API_ENDPOINT"] # receiving server
            self.DEVICE = data["DEVICE"]        # arduino device ie /dev/ttyACM0 ( uno ), /dev/ttyUSB0 (nano)
            self.FILENAME = data["FILENAME"]    # json file ( ie. nginx served)
            self.LOCATION = data["LOCATION"]    # kök
            self.SENSOR = data["SENSOR"]        # identifer : idX-SENSOR
            self.BUFFERSIZE = data["BUFFERSIZE"] # 200 bytes per read
            self.READSPEED = data["READSPEED"]  # 9600 (baud)
            self.TIMEOUT = data["TIMEOUT"]      # 5 (seconds)
            self.TESTDIR = data["TESTDIR"]      # Directory for test files
            self.PRINTMSG = data["PRINTMSG"]    # Y/N
