from simple_async_calculator.enums.operator import Operator


class UnsupportedOperation(Exception):
    """Исключение для неподдерживаемой операции"""


def calculate(*, x: int, y: int, operator: Operator) -> float:
    """Вычисление результата калькулятора"""
    match operator:
        case Operator.SUMMATION:
            return x + y
        case Operator.SUBTRACTION:
            return x - y
        case Operator.DIVISION:
            return x / y
        case Operator.MULTIPLICATION:
            return x * y
        case _:  # pragma: no cover
            raise UnsupportedOperation
