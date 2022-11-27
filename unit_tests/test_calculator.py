import pytest

from simple_async_calculator.enums.operator import Operator
from simple_async_calculator.services.calculator import UnsupportedOperation, calculate


@pytest.mark.parametrize(
    "operator,result",
    [
        (Operator.SUMMATION.value, 10),
        (Operator.SUBTRACTION.value, 6),
        (Operator.MULTIPLICATION.value, 16),
        (Operator.DIVISION.value, 4),
    ],
)
def test_calculate_function(operator, result):
    """Юнит-тест функции расчетов"""
    # act
    calc_result = calculate(x=8, y=2, operator=operator)

    # assert
    assert calc_result == result


def test_calculate_function__invalid_operator():
    """Проверка корректного исключения, если в у задачи БД появилась некорректная операция"""
    # assert
    with pytest.raises(UnsupportedOperation):
        calculate(x=8, y=2, operator="%")
