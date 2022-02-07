from check import temp_value
from check import pressure_value
from check import humidity_value
from check import ds18b20_sensors_parse
from check import DataError
from config import Config


import unittest


class MyTestCase(unittest.TestCase):

    # temperature data

    # Returns true if temp_value("val") raises an Exception
    def test_1(self):
        with self.assertRaises(ValueError):
            temp_value("12. 2")

    def test_2(self):
        with self.assertRaises(ValueError):
            temp_value("")

    def test_3(self):
        with self.assertRaises(ValueError):
            temp_value("      ")

    def test_4(self):
        with self.assertRaises(ValueError):
            temp_value("     ")

    def test_5(self):
        with self.assertRaises(ValueError):
            temp_value("  .  ")

    def test_6(self):
        with self.assertRaises(ValueError):
            temp_value("1")

    def test_7(self):
        with self.assertRaises(ValueError):
            temp_value("12345")

    def test_8(self):
        with self.assertRaises(ValueError):
            temp_value("12. 1")

    def test_9(self):
        with self.assertRaises(ValueError):
            temp_value("12.  ")

    def test_10(self):
        with self.assertRaises(ValueError):
            temp_value("12.444")

    def test_11(self):
        with self.assertRaises(ValueError):
            temp_value("AB.CD")

    def test_12(self):
        with self.assertRaises(ValueError):
            temp_value("1A.21")

    # Pressure data
    def test_20(self):
        with self.assertRaises(ValueError):
            pressure_value("1000")

    def test_21(self):
        with self.assertRaises(ValueError):
            pressure_value("10000.00")

    def test_22(self):
        with self.assertRaises(ValueError):
            pressure_value("999.000")

    def test_23(self):
        with self.assertRaises(ValueError):
            pressure_value("999.0A")

    # Humidity data
    def test_30(self):
        with self.assertRaises(ValueError):
            humidity_value("1000")

    def test_31(self):
        with self.assertRaises(ValueError):
            humidity_value("10000.00")

    def test_32(self):
        with self.assertRaises(ValueError):
            humidity_value("999.000")

    def test_33(self):
        with self.assertRaises(ValueError):
            humidity_value("99.0A")

    def test_34(self):
        with self.assertRaises(ValueError):
            humidity_value("1")

    def test_40(self):
        conf = Config()
        self.assertIsNot(conf.READSPEED, 0, "OK")

    def test_50(self):
        conf = Config()
        with self.assertRaises(DataError):
            fd = open(conf.TESTDIR + "1.err", "r")
            buff: str = fd.read()
            fd.close()
            ds18b20_sensors_parse(buff)

    def test_51(self):
        conf = Config()
        with self.assertRaises(DataError):
            fd = open(conf.TESTDIR + "2.err", "r")
            buff: str = fd.read()
            fd.close()
            ds18b20_sensors_parse(buff)

    def test_52(self):
        conf = Config()
        with self.assertRaises(DataError):
            fd = open(conf.TESTDIR + "3.err", "r")
            buff: str = fd.read()
            fd.close()
            ds18b20_sensors_parse(buff)

    def test_53(self):
        conf = Config()
        fd = open(conf.TESTDIR + "1.ok", "r")
        buff: str = fd.read()
        fd.close()
        expected = ['{ "id" :1, "temp" :22.12}', ',{ "id" :2, "temp" :26.69}', ',{ "id" :3, "temp" :19.44}']
        result = ds18b20_sensors_parse(buff)
        self.assertEqual(expected,result)


if __name__ == '__main__':
    unittest.main()
