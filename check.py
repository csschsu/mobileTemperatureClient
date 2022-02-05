#!/usr/bin/python3

def temp_value(s):
    if len(s) != 5:
         raise ValueError
    if s[2] != ".":
         raise ValueError
    for char in s:
         if char.isdigit() == False and char != ".":
             raise ValueError
    return


