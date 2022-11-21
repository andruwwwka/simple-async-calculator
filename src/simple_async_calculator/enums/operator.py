from enum import Enum


class Operator(str, Enum):
    summation = '+'
    subtraction = "-"
    multiplication = "*"
    division = "/"
