"""Модульные тесты pytest для задания №3 средней сложности."""

import pytest

from simple_function_pytest import (
    add_numbers,
    calculate_average,
    calculate_discounted_price,
)


@pytest.mark.parametrize(
    "first,second,expected",
    [
        (0, 0, 0.0),
        (10, 25, 35.0),
        (-5.5, 2.5, -3.0),
        (100.1, 0.9, 101.0),
    ],
)
def test_add_numbers_parametrized(
    first: float, second: float, expected: float
) -> None:
    """Проверяет функцию сложения на наборе параметризованных значений."""
    assert add_numbers(first, second) == pytest.approx(expected)


def test_add_numbers_rejects_invalid_types() -> None:
    """Проверяет отклонение некорректных типов аргументов в add_numbers."""
    with pytest.raises(TypeError):
        add_numbers(False, 5)
    with pytest.raises(TypeError):
        add_numbers("10", 5)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "price,discount,expected",
    [
        (1000.0, 0.0, 1000.0),
        (1000.0, 20.0, 800.0),
        (199.99, 10.0, 179.99),
        (750.0, 100.0, 0.0),
    ],
)
def test_calculate_discounted_price(
    price: float, discount: float, expected: float
) -> None:
    """Проверяет расчёт цены со скидкой на различных входных данных."""
    assert calculate_discounted_price(price, discount) == pytest.approx(
        expected
    )


def test_calculate_average_values_and_empty() -> None:
    """Проверяет вычисление среднего значения и реакцию на пустой список."""
    assert calculate_average([10.0, 20.0, 30.0]) == pytest.approx(20.0)
    with pytest.raises(ValueError):
        calculate_average([])
