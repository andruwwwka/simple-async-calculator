from enum import Enum


class Operator(str, Enum):
    """Доступные операторы математических операций"""

    SUMMATION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"
