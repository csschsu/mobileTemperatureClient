from check import temp_value

import unittest

class MyTestCase(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()

