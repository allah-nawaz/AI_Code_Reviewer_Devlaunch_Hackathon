# This is a sample Python file for testing the reviewer
# It intentionally contains bad practices and issues for review tools

from math import *
import os, sys, json  # multiple imports on one line
from datetime import datetime
import random as r

GLOBAL_VAR = 10
debug = True


def long_function():
    # Very long function (should be split)
    for i in range(60):
        print("Line", i)

    temp = 0
    for i in range(1000000):  # Performance issue
        temp += i

    if debug == True:  # Bad boolean comparison
        print("Debug mode is on")

    unused_variable = 123  # Unused variable
    return temp


password = "secret123"  # Hardcoded password (security issue)
API_KEY = "ABC123-SECRET-KEY"  # Another secret in code


eval("print('Hello from eval')")  # Insecure eval
exec("x = 5")  # Insecure exec


def bad_naming(x, y):
    z = x + y
    return z


def divide(a, b):
    return a / b  # No zero division handling


def file_reader():
    f = open("data.txt", "r")  # File not closed
    data = f.read()
    return data


def write_file():
    with open("output.txt", "w") as f:
        f.write("Hello")
        f.close()  # Redundant close inside context manager


class user:  # Class name should be Capitalized
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        print("User:", self.name, self.age)


def duplicate_logic(a):
    if a > 10:
        print("Big number")
    else:
        print("Small number")


def duplicate_logic_again(a):  # Duplicate code
    if a > 10:
        print("Big number")
    else:
        print("Small number")


try:
    risky = 10 / 0
except:
    pass  # Bare except, hides real errors


def too_many_args(a, b, c, d, e, f, g, h):
    return a + b


def magic_numbers():
    return 42 * 3.14 / 7  # Magic numbers


def mutable_default(arg=[]):  # Dangerous default
    arg.append(1)
    return arg


def sql_query(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"  # SQL injection risk
    return query


print("Random:", r.randint(1, 10))
