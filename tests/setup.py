import os
import sys


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))


class Case():
    def __init__(self, name: str,  input: dict, expected: dict):
        self.name = name
        self.input = input
        self.expected = expected


class Request():
    def __init__(self, headers: dict = {}, cookies: dict = {}):
        self.headers = headers
        self.cookies = cookies
