"""Задание №3 (средней сложности): Написать простую функцию и тест pytest."""

from typing import Sequence
import pytest


def add_numbers(first: float, second: float) -> float:
    """Возвращает сумму двух чисел с проверкой типов аргументов."""
    if isinstance(first, bool) or isinstance(second, bool):
        raise TypeError("Логический тип bool не допускается для сложения")
    if not isinstance(first, (int, float)) or not isinstance(
        second, (int, float)
    ):
        raise TypeError("Аргументы должны быть числами (int или float)")
    return float(first + second)


def calculate_discounted_price(price: float, discount_percent: float) -> float:
    """Вычисляет итоговую стоимость товара с учётом процентной скидки."""
    if isinstance(price, bool) or isinstance(discount_percent, bool):
        raise TypeError("Параметры цены и скидки должны быть числами")
    if price < 0:
        raise ValueError("Цена товара не может быть отрицательной")
    if not 0.0 <= discount_percent <= 100.0:
        raise ValueError("Процент скидки должен находиться в [0, 100]")
    factor = 1.0 - (discount_percent / 100.0)
    return round(price * factor, 2)


def calculate_average(values: Sequence[float]) -> float:
    """Вычисляет среднее арифметическое непустой последовательности чисел."""
    if not values:
        raise ValueError("Невозможно вычислить среднее для пустого списка")
    return sum(values) / len(values)


def test_add_numbers_basic() -> None:
    """Проверяет сложение положительных, отрицательных и дробных чисел."""
    assert add_numbers(2, 3) == 5.0
    assert add_numbers(-10, 4) == -6.0
    assert add_numbers(1.25, 2.75) == pytest.approx(4.0)


def test_calculate_discounted_price_valid() -> None:
    """Проверяет расчёт скидки для граничных и стандартных значений."""
    assert calculate_discounted_price(1000.0, 15.0) == pytest.approx(850.0)
    assert calculate_discounted_price(500.0, 0.0) == pytest.approx(500.0)
    assert calculate_discounted_price(500.0, 100.0) == pytest.approx(0.0)


def test_calculate_discounted_price_errors() -> None:
    """Проверяет генерацию исключений при некорректной цене или скидке."""
    with pytest.raises(ValueError):
        calculate_discounted_price(-100.0, 10.0)
    with pytest.raises(ValueError):
        calculate_discounted_price(100.0, 120.0)
    with pytest.raises(TypeError):
        calculate_discounted_price(True, 10.0)


def main() -> None:
    """Демонстрирует работу чистых функций расчёта в консольном режиме."""
    print("Демонстрация функций модуля simple_function_pytest:")
    sum_result = add_numbers(12.5, 7.5)
    print(f"  1. Сумма чисел add_numbers(12.5, 7.5) = {sum_result:.2f}")
    if sum_result != 20.0:
        raise RuntimeError("Ошибка расчёта суммы чисел")

    final_price = calculate_discounted_price(2400.0, 25.0)
    print(
        f"  2. Цена со скидкой calculate_discounted_price(2400, 25%) = "
        f"{final_price:.2f} руб."
    )
    if final_price != 1800.0:
        raise RuntimeError("Ошибка расчёта цены со скидкой")

    grades = [4.5, 5.0, 4.8, 4.9]
    avg_grade = calculate_average(grades)
    print(f"  3. Средний балл для {grades} = {avg_grade:.2f}")
    print("Для запуска модульных тестов выполните: pytest")


if __name__ == "__main__":
    main()
